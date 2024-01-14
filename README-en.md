# Learn about your City from Data 'Machi Learn'

[日本語版Readme](README.md)

Created for Urban Data Challenge 2023 application. Basically it's about analysis of elections, population, facilities and so on of Nishitokyo, Tokyo, which where I live, it also has a function enabling an extension for other cities.

URL: https://machiran.onrender.com

The load can be slow due to the server limitation.



## Tools
Python only. `Dash` and `Plotly` were used.

### Versions (main ones only)
```
python==3.9.18
dash==2.14.2
dash_bootstrap_components==1.5.0
dash_daq==0.5.0
dash-core-components==2.0.0
plotly==5.18.0
geopandas==0.14.2
nlplot==1.6.0
```



## Contents
### Politics
+ Graphs on vote rates and attributes of candidates in the former 6 City Elections held in Nishitokyo
+ A network-graph on what has been discussed in Nishitokyo City Council starting from 2001
+ A section where formatted-as-ordered data uploads enable a part of analysis and visualizations introduced above


### City
+ Graphs on population of Nishitokyo and its shift over a period
+ An on-map visualization of facilities, shelters and emergecy routes existing in Nishitokyo
+ A section where formatted-as-ordered data uploads enable analysis and visualizations introduced above


## Favorite Points
+ Interactive visualization of data such as City Council election result, which have conventionally been visualized only in stable context like in PDF
+ Extendabilty to other municipalities than Nishitokyo



## Overview
### Title Page
![スクリーンショット (617)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/623ab034-d6b1-482b-85fd-500cb460c54d)


### Politics
![スクリーンショット (618)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/f9ecc9b9-a054-4445-bdaf-6da2421209ee)


#### ☆Basic Statistical Figures
The distribution of parties, sex, age and election result of Nishitokyo City Council candidates, and vote rate/ number in City Council and Mayor elections. 
A municipality-wise extension prepared.

![スクリーンショット (619)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/f8c78e07-22f1-4f0f-9f3c-6ead22e3bdd5)


#### Candidates Name, Pledges and other info
A table summarizing names, ages, parties, pledges explained in election gazettas, careers, results in the previous election and the results. 

![スクリーンショット (620)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/4e1e687a-0290-4f6c-9390-6159ebc5f394)


#### ☆Relationship between multiple attributes and the Election Result
A graph which indicates the relationship between kinds of attributes (age, sex, party, received vote/ vote rate, received vote/ vote rate in the previous election, result in 
the previous election) and the results in the election held in the selected year. A municipality-wise extension prepared.

![スクリーンショット (630)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/8aa9bb1e-0ea7-42e7-a15b-2fd522c3c878)


#### City Council Review
A network graph which shows the important vocabularies in Nishitokyo City Council and their links.

![スクリーンショット (621)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/073f6301-0bea-471c-9ae1-2ea9ca14a0d9)


#### Make graphs of your city!
Data upload section for  municipality-wise-extension-prepared graphs (ones marked with ☆). You can test this with files in `assets`.

![スクリーンショット (622)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/21a2977f-5093-40ff-b586-5396f341bf55)


### City

![スクリーンショット (623)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/770a14e9-f425-4ff5-b806-47e327754656)


#### ☆Basic Statistical Figures
The population of Nishitokyo and its shift over a period. A municipality-wise extension prepared.

![スクリーンショット (624)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/0221a59b-b95d-4641-af93-eab081786a29)


#### ☆City Features
A visualization of landmarks, railway stations, shelters, emergency routes, municipal border, parks and share cycle station by [PLATEAU](https://www.mlit.go.jp/plateau/)
open data etc. A municipality-wise extension prepared.

![スクリーンショット (625)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/c962fb91-3005-4d31-b34f-5898ae0d8849)


#### Make graphs of your city!
Data upload section for  municipality-wise-extension-prepared graphs (ones marked with ☆). Below is the visualization of Tokyo 23 wards (tested with the data of Sapporo too). You can test this with files in `assets`.


![スクリーンショット (633)](https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-/assets/156287780/773d3201-3ed5-48dc-a5b7-806466fcefe6)



## Data Source
Open data source.

1. [Nishitokyo　Former Elections](https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html)
2. [Nishitokyo　Council Minutes](https://www.city.nishitokyo.tokyo.dbsr.jp/index.php/)
3. [Nishitokyo　Population, Number of Households](https://www.city.nishitokyo.lg.jp/siseizyoho/tokei/zinko/index.html)
4. [PLATEAU　Open Data-Other Data Set](https://www.mlit.go.jp/plateau/)
5. [ODPT　Share Cycle Station Data](https://www.odpt.org/2022/06/28/press20220628_bikeshare/)



## Definition of Values, Aigorithm and so on
Noted in within the site.



## Execution in a local computer
Though you may not have to take a trouble of executing locally, in case the site won't appear, please refer here.


### Preparation
An environment with Python lower than version 3.12. (Development env is Python 3.9.18. Though not tested with all the versions lower than 3.12, successfully executed with 3.9.2.)


### Windows (Tested in Edition:	Windows 11 Home, Version:	23H2, OS build:	22631.3007)
Run as follows.


#### 1. Clone this repository
You will need to install [Git for Windows](https://gitforwindows.org/) for cloning.
```
git clone https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-.git
```


#### 2. Execution
Run the following in their order.
```
cd C:\Users\USERNAME\Learning-about-City-from-Data_-Machi-Learn-
pip install -r requirements.txt
python app.py
```

If `Dash is running on http://0.0.0.0:5000/` is shown, it's successful. Please open in a browser. Tested browsers are Google Chrome, Microsoft Edge. If the page doesn't appear, open `http://localhost:5000` instead.



## Licence
MIT
