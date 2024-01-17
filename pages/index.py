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
    ], style={'margin': 0, 'position': 'relative', 'top': '40%', 'transform': 'translateY(-50%)', 'left':'30vw'}),

    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **まちラーンでは各ページに表示されている、西東京市のデータに基づいた分析結果を見るのはもちろんのこと、**
            
            **自分で作成したデータセットをアップロードすることで、それらと同様の分析をほかの自治体に対して行うこともできます。**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '1.6vw', 'color': 'black', 'width':'90%'}
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




