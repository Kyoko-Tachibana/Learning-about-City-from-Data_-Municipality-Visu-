# データで街について学べるサイト「まちラーン」
Urban Data Challenge 2023 への応募のため作成したものです。ベースは私の居住地である東京都西東京市の選挙や人口、施設についての分析ですが、それをほかの自治体にも応用できるような機能も搭載しています。

URLはこちら https://machiran.onrender.com

サーバーの都合上、ロードが遅い場合があります。




## 使用ツール
Python only で、`Dash`, `Plotly` を中心に用いました。初学者の私にとっても非常に使いやすかったです。



## コンテンツ
### 政治
+ 過去6回の西東京市議会議員選挙、市長選挙の投票率や立候補者の属性についてのグラフ
+ 2001年からの西東京市議会で、どのような議論が行われてきたのかについてのネットワークグラフ
+ 指定されたフォーマットに従って作成したデータをアップロードすると、上記の分析・可視化の一部をほかの自治体について行えるセクション


### 都市
+ 西東京市の人口・人口構成の推移についてのグラフ
+ 西東京市に存在する施設、避難所、避難経路の地図上への可視化
+ 指定されたフォーマットに従って作成したデータをアップロードすると、上記の分析・可視化をほかの自治体について行えるセクション



## 推しポイント
+ 従来PDF上のグラフなど、ほとんどのケースで静的な可視化しかされてこなかった市議会議員選挙などのデータを、動的に可視化している点
+ 西東京市以外の自治体にも拡張できる点



## Overview
### タイトルページ
![スクリーンショット (617)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/623ab034-d6b1-482b-85fd-500cb460c54d)


### 政治
![スクリーンショット (618)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/f9ecc9b9-a054-4445-bdaf-6da2421209ee)


#### ☆Basic Statistical Figures
西東京市議会議員選挙立候補者の所属政党、性別、年齢、当落の分布および市議会議員選挙・市長選挙の投票率・数。他自治体分析対応。

![スクリーンショット (619)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/f8c78e07-22f1-4f0f-9f3c-6ead22e3bdd5)


#### Candidates Name, Pledges and other info
市議会選挙・市長選挙の全候補者の名前、年齢、所属政党、選挙公報掲載の公約、経歴、一つ前の選挙での当落、当落をまとめた表。

![スクリーンショット (620)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/4e1e687a-0290-4f6c-9390-6159ebc5f394)


#### ☆Relationship between multiple attributes and the Election Result
市議会議員選挙立候補者の各種属性（年齢、性別、所属政党、得票率・数、一つ前の選挙での得票率・数、一つ前の選挙での当落）と、該当年の選挙での当落を示すグラフ。他自治体分析対応。

![スクリーンショット (630)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/8aa9bb1e-0ea7-42e7-a15b-2fd522c3c878)


#### City Council Review
西東京市議会議事録における重要語とその分布を示すネットワーク図。

![スクリーンショット (621)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/073f6301-0bea-471c-9ae1-2ea9ca14a0d9)


#### Make graphs of your city!
データアップロード、他自治体分析対応のグラフ（頭に☆がついているもの）の表示。

![スクリーンショット (622)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/21a2977f-5093-40ff-b586-5396f341bf55)


### 都市

![スクリーンショット (623)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/770a14e9-f425-4ff5-b806-47e327754656)


#### ☆Basic Statistical Figures
西東京市の人口・人口構成推移。他自治体分析対応。

![スクリーンショット (624)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/0221a59b-b95d-4641-af93-eab081786a29)


#### ☆City Features
[PLATEAU](https://www.mlit.go.jp/plateau/)のオープンデータなど用いた、ランドマーク、鉄道駅、避難所、緊急避難経路、市の境界、公園、シェアサイクルステーションの可視化。他自治体分析対応。

![スクリーンショット (625)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/c962fb91-3005-4d31-b34f-5898ae0d8849)


#### Make graphs of your city!
データアップロード、他自治体分析対応のグラフ（頭に☆がついているもの）の表示。下では東京23区の情報を可視化しています。

![スクリーンショット (633)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/773d3201-3ed5-48dc-a5b7-806466fcefe6)



## データソース
主に利用したオープンデータソースです。

1. [西東京市　過去の選挙結果](https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html)
2. [西東京市　議会議事録](https://www.city.nishitokyo.tokyo.dbsr.jp/index.php/)
3. [西東京市　人口・世帯数](https://www.city.nishitokyo.lg.jp/siseizyoho/tokei/zinko/index.html)
4. [PLATEAU　オープンデータ-関連データセット](https://www.mlit.go.jp/plateau/)
5. [ODPT　シェアサイクルステーションデータ](https://www.odpt.org/2022/06/28/press20220628_bikeshare/)



## 値の定義、アルゴリズムなど
サイト内に記載があります。



## ローカルでの実行方法
基本的にわざわざローカルで実行する必要はありませんが、サイトがどうしても表示されない場合などはこちらを参照ください。


### 共通の準備
Python 3.12 より低いバージョンで動かせる環境。（開発環境は Python 3.9.18 です。3.12 より低い全てのバージョンで動作テストを行ったわけではありませんが、3.9.2 ではテスト成功しています。）


### Windows (エディション	Windows 11 Home、バージョン	23H2、OS ビルド	22631.3007 にてテスト済み)
以下を実行してください。


#### 1. このリポジトリのクローン
クローンするには、[Git for Windows](https://gitforwindows.org/) というソフトをインストールする必要があります。

`git clone https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-.git`


#### 2. 実行
以下を順に実行してください。

`cd C:\Users\USERNAME\Learning-about-City-from-Data_-Machi-Learn-`

`pip install -r requirements.txt`

`python app.py`

`Dash is running on http://0.0.0.0:5000/` というメッセージが出れば成功です。ブラウザで開いてください。なお、動作が確認されているブラウザは Google Chrome となっています。



## Licence
MIT


