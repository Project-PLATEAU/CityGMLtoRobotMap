import argparse
from pathlib import Path

import open3d
import pymeshlab
import trimesh
import numpy as np
import time

point_set = pymeshlab.MeshSet()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--obj_files', nargs='+', help='list of file path ', required=True)
    parser.add_argument('--save_dir', type=str, default=str(Path.home().joinpath('CG2RM', 'pointcloud')))
    parser.add_argument('-d', '--density', type=float, default=30)
    parser.add_argument('-x',  type=float, default=None, help='box cut x length')
    parser.add_argument('-y',  type=float, default=None, help='box cut y length')

    args = parser.parse_args()

    input_files = [Path(file_str) for file_str in args.obj_files]
    save_directory = Path(args.save_dir)

    save_directory.mkdir(exist_ok=True, parents=True)
    t_start = time.time()

    for input_obj_file in input_files:
        mesh = trimesh.load_mesh(str(input_obj_file), file_type='obj')  # type:trimesh.base.Trimesh
        if isinstance(mesh, trimesh.Scene):
            mesh = trimesh.util.concatenate([trimesh.Trimesh(vertices=m.vertices, faces=m.faces) for m in mesh.geometry.values()])

        print('load', str(input_obj_file), 'bbox size', mesh.bounds)

        if args.x is not None and args.y is not None:

            box = trimesh.creation.box(extents=[args.x * 2, args.y * 2, 1000])
            mesh = mesh.slice_plane(box.facets_origin, -box.facets_normal)

        full_area_size = int(mesh.area)
        density = args.density
        print('all mesh plane area size: {}, density: {} '.format(full_area_size, density))

        components = mesh.split(only_watertight=False)

        print('Number of components:', len(components))
        components_len = len(components)

        components = sorted(components, key=lambda x: (x.area), reverse=True)

        point_numpy = None
        for i, component in enumerate(components):
            area_size = int(component.area)
            sample_number = int(int(component.area) * density)
            sample_number = sample_number if sample_number > 0 else 1

            if sample_number == 1:
                print('Component', i, '/', components_len, ' skip sampling {} points ....'.format(sample_number))
                continue

            # if sample_number > 100000:
            #     spacing = 10
            #     voxel = component.voxelized(pitch=spacing)
            #     slices = trimesh.intersections.slice_mesh_plane(voxel,plane_origin=[0,0,0,],plane_normal = [1,0,0])
            #
            # box = trimesh.creation.box(extents=[1.5, 1.5, 1.5])

            v = component.vertices
            f = component.faces

            if not np.any(component.faces) or not np.any(component.vertices):
                print('Component', i, '/', components_len, ' skip sampling: vertex or faces are empty')
                continue

            pm_mesh = pymeshlab.Mesh(vertex_matrix=component.vertices, face_list_of_indices=component.faces)

            ms = pymeshlab.MeshSet()
            ms.add_mesh(pm_mesh)

            print('Component', i, '/', components_len, ' sampling {} points ....'.format(sample_number))
            ms.generate_sampling_poisson_disk(samplenum=sample_number)

            if point_numpy is None:
                point_numpy = ms.current_mesh().vertex_matrix()
            else:
                point_numpy = np.concatenate([point_numpy, ms.current_mesh().vertex_matrix()])

        ply_file = str(save_directory.joinpath(input_obj_file.name.replace('.obj', '_sample.ply')))
        pcd_file = str(save_directory.joinpath(input_obj_file.name.replace('.obj', '_sample.pcd')))

        save_set = pymeshlab.MeshSet()
        save_set.add_mesh(pymeshlab.Mesh(vertex_matrix=point_numpy))
        save_set.save_current_mesh(ply_file, save_face_color=False)

        open3d.io.write_point_cloud(pcd_file, open3d.io.read_point_cloud(ply_file))
        print('save files: {}'.format(pcd_file))

    t_end = time.time()
    elapsed_time = t_end - t_start
    print('processing time: {}'.format(elapsed_time))
