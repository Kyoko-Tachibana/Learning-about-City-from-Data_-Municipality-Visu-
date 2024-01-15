#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


#layout = html.Div([
 #   html.Div(dcc.Markdown('''
  #  **『まちラーン』**
   # ''', 
    #style={'textAlign':'center', 'font-family':'游明朝', 'font-size':40, 'background-color':'lavender'
     #      }), 
      #     style={'color':'midnightblue', 'position':'relative', 'left':400, 'top':190, 'width': '400px', 'height':'100px',
       #           }),
    #html.Div(dcc.Markdown('''
    #**まちラーンでは各ページに表示されている、西東京市のデータに基づいた分析結果を見るのはもちろんのこと、**
                          
    #**自分で作成したデータセットをアップロードすることで、それらと同様の分析をほかの自治体に対して行うこともできます。**
    #''', 
    #style={'textAlign':'center', 'font-family':'游明朝', 'font-size':15})
     #      , style={'position':'relative', 'top':190, 'left':200, 'width':'810px', 'color':'black'}),
    #dbc.Button('政治', href = '/politics', outline=True, 
     #          style={'font-family': 'Yu Gothic', 'font-size':30, 'textAlign':'center', 'position':'relative'
      #                , 'top':200, 'left':300}, color='light', size='lg'),
    #dbc.Button('都市', href = '/city', outline=True,
     #          style={'font-family': 'Yu Gothic', 'font-size':30, 'textAlign':'center',
      #          'position':'relative', 'top':200, 'left':650}, color='light', size='lg')
#], style={'background-image':'url(assets/city_img.jpg)', 'height':'100%', 
 #         'background-size': 'cover', 'background-position':'center', 'margin-bottom':0, 
  #        'margin-right':0})

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **『まちラーン』**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '4.5vw', 'color': 'midnightblue', 
               'background-color':'lavender', 'width':'40vw'}
        )),
    ], style={'margin': 0, 'position': 'relative', 'top': '40%', 'transform': 'translateY(-50%)', 'left':'35vw'}),

    dbc.Row([
        dbc.Col(dcc.Markdown('''
            **まちラーンでは各ページに表示されている、西東京市のデータに基づいた分析結果を見るのはもちろんのこと、**
            
            **自分で作成したデータセットをアップロードすることで、それらと同様の分析をほかの自治体に対して行うこともできます。**
        ''', 
        style={'textAlign': 'center', 'font-family': '游明朝', 'font-size': '1.42vw', 'color': 'black', 'width':'70%'}
        )),
    ], style={'margin': 0, 'position': 'relative', 'top': '40%', 'transform': 'translateY(-50%)', 'left':'20vw'}),

    dbc.Row([
        dbc.Col(dbc.Button('政治', href='/politics', outline=True, 
               style={'font-family': 'Yu Gothic', 'font-size': '4vw', 'textAlign': 'center'}, color='light', size='lg')),
        dbc.Col(dbc.Button('都市', href='/city', outline=True,
               style={'font-family': 'Yu Gothic', 'font-size': '4vw', 'textAlign': 'center'}, color='light', size='lg')),
    ], style={'margin': 0, 'position': 'relative', 'top': '40%', 'transform': 'translateY(-50%)', 'left':'20%'}),

], style={'background-image': 'url(assets/city_img.jpg)', 'height': '100vh', 
          'background-size': 'cover', 'background-position': 'center', 'margin': 0})




# In[ ]:




