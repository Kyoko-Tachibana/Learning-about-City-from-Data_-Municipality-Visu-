#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **『自治体Visu』**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '4.5vw', 'color': 'midnightblue', 
               'background-color':'lavender', 'width':'40vw'}
        )),
    ], style={'margin': 0, 'position': 'relative', 'top': '33%', 'transform': 'translateY(-50%)', 'left':'30vw'}),

    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **政治、都市の二分野で西東京市のデータを可視化するほか、アップロードされたデータを可視化します。**
            
            **また、それらの可視化結果は各種プラットフォームに統合可能な形式でダウンロードできます。**
            
            **ご自身の自治体を魅力的に外部に発信したい方向けのサービスです。**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '1.6vw', 'color': 'black', 'width':'92%'}
        )),
    ], style={'margin': 0, 'position': 'relative', 'top': '37%', 'transform': 'translateY(-50%)', 'left':'5vw'}),

    dbc.Row([
        dbc.Col(dbc.Button('政治', href='/politics', outline=True, 
               style={'font-family': '游明朝', 'font-size': '3.5vw', 'textAlign': 'center', 'color':'navy'}, 
                           color='light', size='lg')),
        dbc.Col(dcc.Markdown('''
        **ガイド**
        ''', id='guide', style={'color':'deeppink', 'font-size':'3vw', 'background-color':'lavender'})),
        dbc.Col(dbc.Button('都市', href='/city', outline=True,
               style={'font-family': '游明朝', 'font-size': '3.5vw', 'textAlign': 'center', 'color':'navy'}, 
                           color='light', size='lg')),
    ], style={'margin': 0, 'position': 'relative', 'top': '45%', 'transform': 'translateY(-50%)', 'left':'8vw'}),
    
    dbc.Tooltip(dcc.Markdown('''
    ①「都市」「政治」どちらかのボタンを押してスタート！

    ②最初に表示されているのは西東京市のデータを可視化したグラフです。グラフは触って動かすことが出来ます。気になるグラフを探してみましょう。

    ③気になるグラフを見つけたら、自分の自治体用にそのグラフを作ってみましょう！ 指定されているフォーマットに従ってデータを作成、アップロードします。
    （西東京市の方は、表示されているグラフをそのままダウンロードできます。また、一部アップロード機能に対応していないグラフがあります。）

    ④表示されたグラフは、様々な用途に活用できる形式でダウンロードできます。いろいろな使い方を探してみてください！
    ''', style={'font-size':'15px', 'color':'black', 'font-family':'游明朝', 'width':'30vw'}), 
                target='guide', placement='top')

],style={'background-image': 'url(assets/city_img.jpg)', 'height': '100vh', 
          'background-size': 'cover', 'background-position': 'center', 'margin': 0, 'overflow-x': 'hidden'}, lang='ja')




# In[ ]:




