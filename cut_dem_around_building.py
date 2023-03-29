import argparse
from pathlib import Path

import trimesh
from trimesh import creation

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dem', type=str, required=True)
    parser.add_argument('--building', type=str, required=True)
    parser.add_argument('--margin_ratio', type=float, default=1.5)
    parser.add_argument('--save_dir', type=str, default=str(Path.home().joinpath('CG2RM', 'obj')))
    args = parser.parse_args()

    bldg_obj = trimesh.load_mesh(str(args.building), file_type='obj')  # type:trimesh.base.Trimesh
    dem_obj = trimesh.load_mesh(str(args.dem), file_type='obj')  # type:trimesh.base.Trimesh

    print('building bounds', bldg_obj.bounds)
    bounds = bldg_obj.bounds
    r = args.margin_ratio
    box_size = [(bounds[1][0] - bounds[0][0]) * r, (bounds[1][1] - bounds[0][1]) * r, (bounds[1][2] - bounds[0][2]) * r]
    box = creation.box(extents=box_size)

    result = dem_obj.slice_plane(box.facets_origin, -box.facets_normal)
    save_file_path = args.save_dir + 'cut_dem.obj'
    result.export(save_file_path)

    mesh = trimesh.util.concatenate([bldg_obj, result])
    mesh.show()
