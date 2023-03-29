# CityGMLとBIMの位置合わせ

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