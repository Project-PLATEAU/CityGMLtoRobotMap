# 複数の点群を一つの点群にまとめる

複数の点群ファイルを一つに統一する場合、以下のようにコマンドを実行することで統合することが可能です。
````
python3 merge_multi_point_cloud.py -f file_1.pcd file_2.pcd ...
````
オプション
```
usage: merge_multi_point_cloud.py [-h] -f POINT_CLOUD_FILES [POINT_CLOUD_FILES ...] [-t {ply,pcd}] [--save_dir SAVE_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -f POINT_CLOUD_FILES 統合したい点群ファイルのリスト
  -n NAME, --name NAME 
  --save_dir SAVE_DIR

```