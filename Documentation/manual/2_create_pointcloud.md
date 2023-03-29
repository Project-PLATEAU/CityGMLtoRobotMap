# obj から点群を生成

生成したobjファイルのメッシュ表面をサンプリングすることで点群を生成します。densityは面積あたりにサンプリングする点群の数の目安です。
コマンドを実行すると$HOME/CG2RM/pointcloud の中にply,とpcdファイルが生成されます。plyファイルは[cloud comapre](https://www.danielgm.net/cc/)などで表示して確認が可能です。
```
python create_sampling_point_cloud.py -f $HOME/CG2RM/obj/obj_file.obj --density 30
```

オプション
```
usage: create_sampling_point_cloud.py [-h] -f POINT_CLOUD_FILES [POINT_CLOUD_FILES ...] [--save_dir SAVE_DIR] [-d DENSITY]

optional arguments:
  -h, --help            show this help message and exit
  -f POINT_CLOUD_FILES 変換対象のobjファイルのパス。同時に複数指定できます。
  --save_dir SAVE_DIR
  -d DENSITY, --density DENSITY　面積あたりにサンプリングする点群の数
  -x X                  対象メッシュの範囲を制限する　x[m]　デフォルトでは動作しない
  -y Y                  対象メッシュの範囲を制限する　y[m]　デフォルトでは動作しない

```
