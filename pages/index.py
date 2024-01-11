#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


layout = html.Div([
    html.Div(dcc.Markdown('''
    **『まちラーン』**
    ''', 
    style={'textAlign':'center', 'font-family':'游明朝', 'font-size':40, 'background-color':'lavender'
           }), 
           style={'color':'midnightblue', 'position':'relative', 'left':400, 'top':190, 'width': '400px', 'height':'100px'
                  }),
    html.Div(dcc.Markdown('''
    **まちラーンでは各ページに表示されている、西東京市のデータに基づいた分析結果を見るのはもちろんのこと、**
                          
    **自分で作成したデータセットをアップロードすることで、それらと同様の分析をほかの自治体に対して行うこともできます。**
    ''', 
    style={'textAlign':'center', 'font-family':'游明朝', 'font-size':15})
           , style={'position':'relative', 'top':190, 'left':200, 'width':'800px', 'color':'black'}),
    dbc.Button('政治', href = '/politics', outline=True, 
               style={'font-family': 'Yu Gothic', 'font-size':30, 'textAlign':'center', 'position':'relative'
                      , 'top':200, 'left':300}, color='light', size='lg'),
    dbc.Button('都市', href = '/city', outline=True,
               style={'font-family': 'Yu Gothic', 'font-size':30, 'textAlign':'center',
                'position':'relative', 'top':200, 'left':650}, color='light', size='lg')
], style={'background-image':'url(assets/city_img.jpg)', 'width':1263, 'height':660, 
          'background-size': 'cover', 'background-position':'center', 'margin-bottom':0, 
          'margin-right':0})


# In[ ]:




