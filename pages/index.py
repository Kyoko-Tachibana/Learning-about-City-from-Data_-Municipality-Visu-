#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **『まちラーン』**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '4.5vw', 'color': 'midnightblue', 
               'background-color':'lavender', 'width':'40vw'}
        )),
    ], style={'margin': 0, 'position': 'relative', 'top': '35%', 'transform': 'translateY(-50%)', 'left':'30vw'}),

    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **政治、都市の二分野で西東京市のデータを可視化するほか、アップロードされたデータを可視化します。**
            
            **また、それらの可視化結果を各種プラットフォームに統合可能な形式でダウンロードできます。**
            
            **ご自身の自治体を魅力的に外部に発信したい方向けのサービスです。**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '1.6vw', 'color': 'black', 'width':'92%'}
        )),
    ], style={'margin': 0, 'position': 'relative', 'top': '40%', 'transform': 'translateY(-50%)', 'left':'5vw'}),

    dbc.Row([
        dbc.Col(dbc.Button('政治', href='/politics', outline=True, 
               style={'font-family': '游明朝', 'font-size': '3.5vw', 'textAlign': 'center', 'color':'navy'}, 
                           color='light', size='lg')),
        dbc.Col(dbc.Button('都市', href='/city', outline=True,
               style={'font-family': '游明朝', 'font-size': '3.5vw', 'textAlign': 'center', 'color':'navy'}, 
                           color='light', size='lg')),
    ], style={'margin': 0, 'position': 'relative', 'top': '50%', 'transform': 'translateY(-50%)', 'left':'20vw'}),

],style={'background-image': 'url(assets/city_img.jpg)', 'height': '100vh', 
          'background-size': 'cover', 'background-position': 'center', 'margin': 0, 'overflow-x': 'hidden'}, lang='ja')




# In[ ]:




