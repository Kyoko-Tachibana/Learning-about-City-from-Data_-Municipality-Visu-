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
    ], style={'margin': 0, 'position': 'relative', 'top': '30%', 'transform': 'translateY(-50%)', 'left':'30vw'}),

    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **政治、暮らしの二分野で西東京市のデータを可視化するほか、アップロードされたデータを可視化します。**
            
            **また、それらの可視化結果は各種プラットフォームに統合可能な形式でダウンロードできます。**
            
            **ご自身の自治体を魅力的に外部に発信したい方向けのサービスです。**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '1.6vw', 'color': 'black', 'width':'92%'}
        )),
    ], style={'margin': 0, 'position': 'relative', 'top': '34%', 'transform': 'translateY(-50%)', 'left':'5vw'}),

    dbc.Row([
        dbc.Col(dbc.Button('政治', href='/politics', outline=True, 
               style={'font-family': '游明朝', 'font-size': '3.5vw', 'textAlign': 'center', 'color':'navy'}, 
                           color='light', size='lg'), style={'width':4}),

        
        dbc.Col(dcc.Markdown('''
        **ガイドを見る**
        ''', id='guide', 
        style={'color':'deeppink', 'font-size':'2vw', 'background-color':'lavender', 'font-family':'游明朝',
               'textAlign':'center', 'width':'50%', 'height':'6vh'}), 
                style={'width':4, 'position':'relative', 'top':'50%'}),
        
        dbc.Col(dbc.Button('暮らし', href='/city', outline=True,
               style={'font-family': '游明朝', 'font-size': '3.5vw', 'textAlign': 'center', 'color':'navy'}, 
                           color='light', size='lg'), style={'width':4}),
    ], style={'margin': 0, 'position': 'relative', 'top': '45%', 'transform': 'translateY(-50%)', 'left':'10%'}),
    
    dbc.Tooltip(dcc.Markdown('''
    「暮らし」「政治」どちらかのボタンを押してスタート！
    ''', style={'font-size':'15px', 'color':'black', 'font-family':'游明朝'}), 
                target='guide', placement='bottom', style={'maxWidth':'80vw', 'zIndex': 1000, 'width':'40vw', 
                                                        'height':'60vh'})

],style={'background-image': 'url(assets/city_img.jpg)', 'height': '100vh', 
          'background-size': 'cover', 'background-position': 'center', 'margin': 0, 'overflow-x': 'hidden'}, lang='ja')
