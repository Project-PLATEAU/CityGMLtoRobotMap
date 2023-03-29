# CityGMLをobjに変換

### データ準備
CityGML形式のデータが必要となります。

[3D都市モデル（Project PLATEAU）東京都23区](https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku)からCityGML形式のデータをダウンロード可能です。またレポジトリ内にサンプルデータがありますのでそれを使うことも可能です。

また、東京都以外の都市データも公開されています。[3D都市モデル（Project PLATEAU）ポータルサイト](https://www.geospatial.jp/ckan/dataset/plateau)

### 変換

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

* 地域メッシュについて[こちら](https://nlftp.mlit.go.jp/ksj/old/old_data_mesh.html)

次のコマンドを使用することで生成したobjファイルを表示することができます。
```
python view_obj.py $HOME/CG2RM/obj_file.obj
```
