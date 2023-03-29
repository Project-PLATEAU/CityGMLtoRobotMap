import argparse
from pathlib import Path

import trimesh

parser = argparse.ArgumentParser()
parser.add_argument('obj_file', type=Path)
args = parser.parse_args()

obj_data = trimesh.load_mesh(str(args.obj_file), file_type='obj') # type:trimesh.base.Trimesh

obj_data.visual.face_colors = [200, 200, 200, 100]

obj_data.show(smooth=False)
