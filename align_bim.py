import argparse
import copy
import math
from pathlib import Path

import trimesh
from trimesh import registration, convex
from trimesh.transformations import rotation_matrix, concatenate_matrices, translation_matrix
from trimesh.viewer import SceneViewer
import open3d


def get_homogeneous_matrix(x, y, z, roll, pitch, yaw):
    origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
    Rx = rotation_matrix(math.radians(roll), xaxis)
    Ry = rotation_matrix(math.radians(pitch), yaxis)
    Rz = rotation_matrix(math.radians(yaw), zaxis)
    R = concatenate_matrices(Rx, Ry, Rz)
    T = translation_matrix([x, y, z])

    M = concatenate_matrices(T, R)
    return M


def points_matching(bim_building_mesh, map_mesh: trimesh.points.PointCloud):
    mesh_to_other, _, _ = registration.icp(bim_building_mesh.vertices, map_mesh.vertices,
                                           max_iterations=150, threshold=1e-5,
                                           scale=False, reflection=False)

    return mesh_to_other


def mesh_matching(map_mesh, building_mesh, with_convex=False):
    sample = 500
    icp_first = 1
    icp_final = 200

    if with_convex:
        mesh_to_other, _ = registration.mesh_other(convex.convex_hull(building_mesh), map_mesh, samples=sample, icp_first=icp_first, icp_final=icp_final)
    else:
        mesh_to_other, _ = registration.mesh_other(building_mesh, map_mesh, samples=sample, icp_first=icp_first, icp_final=icp_final)

    return mesh_to_other


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--save_dir', type=str, default=str(Path.home().joinpath('CG2RM', 'transformed')))
    parser.add_argument('--offset', nargs="*", type=float, default=[0, 0, 0, 0, 0, 0], help='a list of float variables')
    args = parser.parse_args()

    save_directory = Path(args.save_dir)
    save_directory.mkdir(exist_ok=True, parents=True)

    source_points_path = Path(args.source)  # ply
    target_points_path = Path(args.target)  # ply

    source_points = trimesh.load_mesh(str(source_points_path), file_type='ply')  # type:trimesh.base.Trimesh
    target_points = trimesh.load_mesh(str(target_points_path), file_type='ply')  # type:trimesh.base.Trimesh

    if 'CG2RM' in str(source_points_path):
        source_mesh_path = Path(str(source_points_path).replace('pointcloud', 'obj').replace('.ply', '.obj').replace('_sample', ''))
        target_mesh_path = Path(str(target_points_path).replace('pointcloud', 'obj').replace('.ply', '.obj').replace('_sample', ''))

        source_mesh = trimesh.load_mesh(str(source_mesh_path), file_type='obj')  # type:trimesh.base.Trimesh
        target_mesh = trimesh.load_mesh(str(target_mesh_path), file_type='obj')  # type:trimesh.base.Trimesh

        if isinstance(target_mesh, trimesh.scene.scene.Scene):
            mesh_list = []
            for mesh in target_mesh.geometry.values():
                if isinstance(mesh, trimesh.Trimesh):
                    mesh_list.append(mesh)

            target_mesh = trimesh.util.concatenate(mesh_list)

        if isinstance(source_mesh, trimesh.scene.scene.Scene):
            mesh_list = []
            for mesh in source_mesh.geometry.values():
                if isinstance(mesh, trimesh.Trimesh):
                    mesh_list.append(mesh)

            source_mesh = trimesh.util.concatenate(mesh_list)

    offset = get_homogeneous_matrix(args.offset[0], args.offset[1], args.offset[2], args.offset[3], args.offset[4], args.offset[5])

    source_mesh.apply_transform(offset)
    source_points.apply_transform(offset)

    original_input_mesh = copy.deepcopy(source_mesh)

    print('aligning, please wait ....')

    trans = points_matching(source_points, target_points)

    print('trans matrix\n', trans)

    source_mesh.apply_transform(trans)
    source_points.apply_transform(trans)

    print('target centroid', target_mesh.centroid, 'source centroid', source_mesh.centroid)
    target_mesh.visual.face_colors = [200, 200, 200, 100]
    source_mesh.visual.face_colors = [200, 200, 100, 100]
    original_input_mesh.visual.face_colors = [200, 100, 100, 100]

    scene = trimesh.Scene([target_mesh, original_input_mesh, source_mesh])
    viewer = SceneViewer(scene=scene)

    # save file
    mesh_file = save_directory.joinpath(str(source_points_path.name.replace('.ply', '_aligned.obj')))
    ply_file = save_directory.joinpath(str(source_points_path.name.replace('.ply', '_aligned.ply')))
    pcd_file = save_directory.joinpath(str(source_points_path.name.replace('.ply', '_aligned.pcd')))

    source_mesh.export(str(mesh_file))
    source_points.export(str(ply_file))
    open3d.io.write_point_cloud(str(pcd_file), open3d.io.read_point_cloud(str(ply_file)))
