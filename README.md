
# FY2022 Project PLATEAU UC22-024「3D都市モデルとBIMを活用したモビリティ自律運行システム」の成果物(CityGMLtoRobotMap)
# CityGMLtoRobotMap
![merged_points](https://user-images.githubusercontent.com/79615787/227793505-539b4446-7bf2-46cc-8d7c-00f4e6bf525a.jpg)

## 1. 概要
「CityGMLtoRobotMap」はCityGMLをRobotが自己位置推定などで使用できる環境地図として変換するためのツール群です。  
以下の機能を提供します。  
- CityGMLからOBJ形式への形式変換・座標変換の機能
- OBJファイルの表面をサンプリングして点群を生成できる機能
- BIMとCityGMLのマージ機能

## 2．「3D都市モデルとBIMを活用したモビリティ自律運行システム」について
### ユースケースの概要
都市部における建設工事では資材運搬等による交通渋滞が課題となります。 そこで、自律運航可能なドローンや無人搬送車両（AGV）の活用による解決が期待されている一方で、自動運転モビリティの運航に必要な地図情報として民間事業者が提供する3Dマップを利用せざるを得ず、精度担保やデータ連携、カバレッジ等の点での課題もあります。 本業務では、LiDARやGPS等のセンサーと3D都市モデルを利用した自己位置測位を組み合わせた運航システムを開発しました。

### 開発システムの概要
「CityGMLtoRobotMap」は、LiDAR SLAMを用いた自律飛行ドローンのために3D都市モデルとBIMモデルを統合した点群マップを提供するツール群です。
本業務では、屋外は3D都市モデル（建築物モデルLOD2-3）を、屋内はBIMモデルを活用してLiDARとGNSS（衛星測位システム）による自己位置推定を行うドローン自律飛行システムを、ロボット・アプリケーションの作成支援ライブラリ・ツール群であるROSを利用して構築しました。  
詳細は[技術実証レポート](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_tech_doc_0046_1_ver01.pdf)を参照してください。

## 3．利用手順

インストール方法・使い方は[こちら](https://project-plateau.github.io/CityGMLtoRobotMap/)を参照してください。

## ライセンス
* 本ツールは、令和4年度 民間ユースケース開発　（UC22-024）「3D都市モデルとBIMを活用したモビリティ自律運行システム」の中で[Sensyn Robotics](https://www.sensyn-robotics.com/)が開発したものです。ソースコードおよび関連ドキュメントの著作権は国土交通省に帰属します。
* 本ドキュメントは[Project PLATEAUのサイトポリシー](https://www.mlit.go.jp/plateau/site-policy/)（CCBY4.0および政府標準利用規約2.0）に従い提供されています。

## 注意事項
* 本レポジトリは参考資料として提供しているものです。動作保証は行っておりません。
* 予告なく変更・削除する可能性があります。
* 本レポジトリの利用により生じた損失及び損害等について、国土交通省はいかなる責任も負わないものとします。

## 参考資料
* 3D都市モデルとBIMを活用したモビリティ自律運行システム技術検証レポート: https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_tech_doc_0046_1_ver01.pdf
* PLATEAU Webサイト Use caseページ「3D都市モデルとBIMを活用したモビリティ自律運行システム」: https://www.mlit.go.jp/plateau/use-case/uc22-024/
* 利用しているライブラリなどへのリンク
  * [cjio](https://github.com/cityjson/cjio) : city jsonを扱うライブラリ
  * [pyproj](https://github.com/pyproj4/pyproj) : 緯度経度、座標変換を扱うライブラリ
  * [trimesh](https://github.com/mikedh/trimesh) : メッシュを扱うライブラリ
  * [open3d](https://github.com/isl-org/Open3D) : 点群、メッシュなどを扱うライブラリ
  * [PyMeshLab](https://github.com/cnr-isti-vclab/PyMeshLab) : MeshLab機能のpythonラッパー
