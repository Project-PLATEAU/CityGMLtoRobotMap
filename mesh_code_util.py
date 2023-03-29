from jpmesh import Angle, Coordinate, FirstMesh, SecondMesh, ThirdMesh, parse_mesh_code


def min_max_bbox(input_code_list: list):
    # get bbox limit for cutting point cloud
    lat_list = []
    lon_list = []
    for input_code in input_code_list:
        mesh_code = parse_mesh_code(str(input_code.code))
        mesh_sw = mesh_code.south_west
        # print('south west ', mesh_sw.lon.degree, mesh_sw.lat.degree)
        mesh_ne = mesh_code.south_west + mesh_code.size
        # print('size', mesh_code.size.lat.degree)
        # print('north east ', mesh_ne.lon.degree, mesh_ne.lat.degree)

        lat_list.extend([mesh_sw.lat.degree, mesh_ne.lat.degree])
        lon_list.extend([mesh_sw.lon.degree, mesh_ne.lon.degree])
    print('lon max\t', max(lon_list), '\tmin', min(lon_list))
    print('lat max\t', max(lat_list), '\tmin', min(lat_list))
    return {'lon': {'max': max(lon_list), 'min': min(lon_list)}, 'lat': {'max': max(lat_list), 'min': min(lat_list)}}


def near_code_search(code):
    code_list = []
    mesh_code = parse_mesh_code(str(code))
    mesh_center = mesh_code.south_west + (mesh_code.size / 2.0)
    d_lat = mesh_code.size.lat.degree
    d_lon = mesh_code.size.lon.degree

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            target_lat = Angle.from_degree(mesh_center.lat.degree + d_lat * i)
            target_lon = Angle.from_degree(mesh_center.lon.degree + d_lon * j)
            near_code = ThirdMesh.from_coordinate(Coordinate(lon=target_lon, lat=target_lat))
            code_list.append(near_code)

    return code_list


def specify_code(lat, lon):
    coordinate = Coordinate(lon=Angle.from_degree(lon), lat=Angle.from_degree(lat))
    fmc = FirstMesh.from_coordinate(coordinate)
    smc = SecondMesh.from_coordinate(coordinate)
    tmc = ThirdMesh.from_coordinate(coordinate)
    return fmc.code, smc.code, tmc.code


if __name__ == '__main__':
    lat_in = 35.6809591
    lon_in = 139.7673068
    # specify code
    first, second, third = specify_code(lat_in, lon_in)

    print('first', first, 'second', second, 'third', third)

    code_list = near_code_search(third)
    print([item.code for item in code_list])
    result_dict = min_max_bbox(code_list)

    ret1 = [item.code for item in code_list]
    ret2 = result_dict
