import argparse
import math
import subprocess
from os.path import exists
from pathlib import Path
from statistics import mean

from cjio import cityjson
from pyproj import Transformer

from mesh_code_util import specify_code


def reproject(CS: cityjson.CityJSON, target_epsg: int):
    CS.decompress()

    from_crs = 'epsg:%d' % (CS.get_epsg())
    to_crs = 'epsg:%d' % (target_epsg)
    transformer = Transformer.from_crs(from_crs, to_crs)
    trans_points = list(transformer.itransform(CS.j['vertices']))
    CS.j['vertices'] = [list(item) for item in trans_points]

    CS.set_epsg(target_epsg)
    CS.update_bbox()
    CS.update_bbox_each_cityobjects(True)

    return CS


def reproject_custom(CS: cityjson.CityJSON, lat: float, lon: float, altitude):
    """'
      https://gis.stackexchange.com/questions/299426/transform-coordinates-from-custom-projection-to-lat-long-pyproj

            std::sprintf(
            proj_enu_crs,"+proj=etmerc +ellps=GRS80 +lon_0=%.10f +lat_0=%.10f +x_0=0 +y_0=0 "
            "+z_0=-%.10f +k_0=1",base_point_longitude_, base_point_latitude_, base_point_altitude_);
    """

    CS.decompress()
    from_crs = 'epsg:%d' % (CS.get_epsg())
    to_crs = "+proj=etmerc +ellps=GRS80 +lon_0={} +lat_0={} +x_0=0 +y_0=0 +z_0={} +k_0=1".format(lon, lat, altitude)

    transformer = Transformer.from_crs(from_crs, to_crs)
    CS.j['vertices'] = [list(item) for item in transformer.itransform(CS.j['vertices'])]
    CS.set_epsg(None)

    CS.update_bbox()
    CS.update_bbox_each_cityobjects(True)


def print_vertex_centroid(CJ: cityjson.CityJSON):
    points = CJ.j['vertices']
    ct = [0, 0, 0]
    ct[0] = mean(list(item[0] for item in points))
    ct[1] = mean(list(item[1] for item in points))
    ct[2] = mean(list(item[2] for item in points))

    print("odj model's centroid", ct)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source_dir', type=str, required=True,
                        help='pass city gml source directory or file. If you pass directory, .gml files in that directory will be serached for and coonverted . If you pass a file,that file will be converted.')
    parser.add_argument('--lat', type=float, default=35.6809591, required=True, help='Latitude')
    parser.add_argument('--lon', type=float, default=139.7673068, required=True, help='Longitude ')
    parser.add_argument('--alt', type=float, default=17.0, required=True, help='Altitude')
    parser.add_argument('--save_dir', type=str, default=str(Path.home().joinpath('CG2RM', 'obj')), help='output directory')
    parser.add_argument('-u', '--update', action='store_true', help='over write already generated cityjson, filterd_lods.gml files.')
    parser.add_argument('--mapcode_level', type=str, default='third', choices=["first", "second", "third"],
                        help='map mesh code. first code include large area. third code include small area.')
    parser.add_argument('--lod', type=str, default=None, choices=["max", "1", "2", "3", "4"],
                        help='extract lods. if use choose 1~4 , this filter only extract same level lods. If you choose max. extract max level lod from same building.')

    args = parser.parse_args()

    first, second, third = specify_code(args.lat, args.lon)
    map_code_dict = {'first': first, 'second': second, 'third': third}

    map_code_number = map_code_dict[args.mapcode_level]  # args.number  # 53392575
    source_dir = args.source_dir
    extension = "*[0-9].gml"
    all_glob_gml_files = []

    if Path(source_dir).is_dir():
        print("Find files include {} in name from  {}".format(map_code_number, source_dir))
        all_glob_gml_files = list(Path(source_dir).rglob(str(map_code_number) + extension))
    elif Path(source_dir).is_file():
        all_glob_gml_files = [Path(args.source_dir)]

    target_part_names = ['bldg', 'brid', 'dem', 'tran']
    convert_target_to_cityjson_files = []

    # search target gml files that have target name
    for path in all_glob_gml_files:
        for item in target_part_names:
            if str(item) in str(path):
                convert_target_to_cityjson_files.append(path)
                print("Convert target to obj :  {}".format(path))

    # filter lods in city gml
    if args.lod is not None:
        lods_dict = {'max': "1,2,3,4", "1": 1, "2": 2, "3": 3, "4": 4}

        for i, gml_file in enumerate(convert_target_to_cityjson_files):
            json_path = str(gml_file).replace('.gml', '.json')
            lod_filterd_gml_file = Path(str(gml_file).replace('.gml', '__filtered_lods.gml'))
            convert_target_to_cityjson_files[i] = lod_filterd_gml_file
            if args.update:
                print("filtering lods {}".format(lod_filterd_gml_file.name))
                output_str = subprocess.run(
                    ["citygml-tools-2.0.0/citygml-tools",
                     "filter-lods",
                     "--lod={}".format(lods_dict[args.lod]),
                     "--mode=maximum",
                     str(gml_file)],
                    capture_output=True, text=True).stderr
                print(output_str)

    # city gml to city json:  no coordinate trans
    for gml_file in convert_target_to_cityjson_files:
        json_path = str(gml_file).replace('.gml', '.json')
        if not exists(json_path) or args.update:
            print("converting  {} to city_json ".format(gml_file.name))

            output_str = subprocess.run(
                ["citygml-tools-2.0.0/citygml-tools",
                 "to-cityjson", "--vertex-precision=15", "--template-precision=15",
                 "--cityjson-version=1.0", str(gml_file)],
                capture_output=True, text=True).stderr
            print(output_str)

        else:
            print(json_path, 'is already exist')

    # transform and generate obj
    obj_save_directory = Path(args.save_dir)
    obj_save_directory.mkdir(exist_ok=True, parents=True)

    for gml_path in convert_target_to_cityjson_files:
        input_gml_file = str(gml_path).replace('.gml', '.json')  # args.city_json_file
        obj_file = obj_save_directory.joinpath(gml_path.name.replace(".gml", ".obj"))

        if exists(obj_file) and (not args.update):
            print(obj_file, 'is already exist')
        else:
            print('converting to ', obj_file)
            with open(input_gml_file, mode='r', encoding='utf-8-sig') as f:
                CJ = cityjson.reader(file=f, ignore_duplicate_keys=True)

            if CJ.is_empty():
                print("WARN :{} has no information. Check file or lod level arg. ".format(input_gml_file))
                continue

            # transform points from EPSG:6697 to base points
            CJ = reproject(CJ, 4326)  # 4326 = wgs84

            reproject_custom(CJ, args.lat, args.lon, args.alt)

            # print_vertex_centroid(CJ)
            result_obj = CJ.export2obj().getvalue()

            with open(obj_file, mode='w') as out_file:
                out_file.write(result_obj)
                print('saved ', obj_file)
