
# 各ツール使用方法・手順
1. CityGMLをobjに変換する機能
2. obj から点群を生成する機能
3. BIM(ifc)をobjに変換する機能 
4. CityGMLとBIMの位置合わせを行う機能   
5. 複数の点群を一つの点群にまとめる機能

(注意：poetryにより構築したpython環境を使うためには`poetry shell`を実行しpoetry環境をactivateする必要があります。)


### 準備
CityGML形式のデータが必要です。

[3D都市モデル（Project PLATEAU）東京都23区](https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku)からCityGML形式のデータをダウンロードし解凍してください。
または、* [Example](EXAMPLE.md)　にあるようにレポジトリ内にあるサンプルデータを使ってください。


また、東京都以外の都市データも公開されています。[3D都市モデル（Project PLATEAU）ポータルサイト](https://www.geospatial.jp/ckan/dataset/plateau)

### 1.CityGMLをobjに変換

以下を実行すると$HOME/CG2RM/obj の中にCityGMLから変換されたobjファイルが生成されます。$HOME/CG2RM/objはプログラムが自動的に作成します。

ここでは「~/Downlods/plateau-tokyo23ku」にデータがあると想定してツール使用時のコマンドを記述します。
指定している緯度経度は 【東京都庁所在地】 緯度：35.6895014 経度：139.6917337 高さ：0 となっています。


```
python gml2obj.py　-s ~/Downlods/plateau-tokyo23ku/udx --lat 35.6895014 --lon 139.6917337 --alt 30 --mapcode＿level third
```
オプション
```
usage: gml2obj.py [-h] -s SOURCE_DIR --lat LAT --lon LON --alt ALT [--save_dir SAVE_DIR] [-u] [--mapcode_level {first,second,third}] [--lod {max,1,2,3,4}]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_DIR, --source_dir SOURCE_DIR　CityGMLを含むディレクトリか、CityGMLファイルを渡してください。ディレクトリであれば自動で内部のCityGMLを探します。
  --lat LAT             Latitude　緯度
  --lon LON             Longitude　経度
  --alt ALT             Altitude 高さ
  --save_dir SAVE_DIR   
  -u, --update          中間生成ファイルを上書きします
  --mapcode_level {first,second,third}　変換対象エリアを定めます。1次メッシュ、2次メッシュ、3次メッシュ
  --lod {max,1,2,3,4}   一つの建物が複数のLODを持つ場合、maxを指定すると一番レベルが高いものを抽出。1,2,3,4いずれかであれば指定のレベルのLODのみ抽出します。

```
大まかな処理の流れ
1. 指定した緯度経度を含む地域メッシュコードを特定
2. 対象のメッシュコードを含むファイルを探索・特定
3. 指定したlod level情報を抽出
4. 指定した緯度経度を原点とした3d情報へと変換
5. objファイルへ変換・保存

* 地域メッシュについて(https://nlftp.mlit.go.jp/ksj/old/old_data_mesh.html)



次のコマンドを使用することで生成したobjファイルを表示することができます。
```
python view_obj.py $HOME/CG2RM/obj_file.obj
```

### 2.obj から点群生成
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


### 3.BIMを使う場合）BIMをobj・点群に変換

BIMをobjに変換する場合はIfcConvertを使用します。以下のようにコマンドで変換を行います。
```
./IfcConvert input_bim.ifc output_obj.obj
```
objに変換された後は、2と同様に点群への変換が可能です。

### 4.（BIMを使う場合）obj(CityGMLから)とobj(BIM)の位置合わせを行う

位置合わせを行いたいCityGMLとBIMとそれぞれから生成された点群を指定し
```
python align_bim.py --source ~/CG2RM/pointcloud/bim_model.ply --target ~/CG2RM/pointcloud/CityGML_model.ply  
```
オプション
```
usage: align_bim.py [-h] --source SOURCE --target TARGET [--save_dir SAVE_DIR] [--offset [OFFSET [OFFSET ...]]]

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE 位置を変化させて位置合わせを行いたい点群
  --target TARGET　位置合わせの基準となる点群
  --save_dir SAVE_DIR
  --offset [x,y,z,ywa,roll,pitch] 位置合わせ前にオフセットさせる際の値
                        

```
コマンドを実行することでCityGMLが持つ座標系に合うように位置調整したBIMが結果として得られます。  
自動調整には限界があるため、うまく一致しない場合はBlenderなどのソフトを使って手動で調整することも可能です。

### 5.複数の点群を一つの点群にまとめる

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