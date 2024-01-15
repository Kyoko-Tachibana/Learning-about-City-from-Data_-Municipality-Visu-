#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly
import plotly.express as px
import dash
from dash import html
from dash import dcc
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import base64
import io
import dash_bootstrap_components as dbc
from dash import callback, State
from dash.dependencies import Input, Output
import dash_daq as daq
from plotly.colors import n_colors
import ipywidgets as widgets
from dash import Dash
import geopandas as gpd
import ast


# In[ ]:
font_fam_sp = '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'

df_border = pd.read_csv('assets/border.csv', encoding='shift-jis')
df_park = pd.read_csv('assets/park.csv', encoding='shift-jis')
df_shelter = pd.read_csv('assets/shelter.csv', encoding='shift-jis')
df_emergency_route = pd.read_csv('assets/emergency_route.csv', encoding='shift-jis')
df_station = pd.read_csv('assets/station.csv', encoding='shift-jis')
df_landmark = pd.read_csv('assets/landmark.csv', encoding='shift-jis')
df_pop = pd.read_csv('assets/Population etc.csv', encoding='shift-jis')
df_hellowcycle = pd.read_csv('assets/ハローサイクリング.csv', encoding='shift-jis')
df_docomo = pd.read_csv('assets/docomo_only_tokyo.csv', encoding='shift-jis')
df_hellowcycle['vehicle_type_capacity'] = df_hellowcycle['vehicle_type_capacity'].apply(ast.literal_eval)

df_shelter['収容人数'] = df_shelter['収容人数'].fillna(0)
df_border['lon'] = df_border['lon'].apply(ast.literal_eval)
df_border['lat'] = df_border['lat'].apply(ast.literal_eval)
df_emergency_route['lon'] = df_emergency_route['lon'].apply(ast.literal_eval)
df_emergency_route['lat'] = df_emergency_route['lat'].apply(ast.literal_eval)

def listrize(x):
    return list(x)

df_border['lon'] = df_border['lon'].apply(lambda x: listrize(x))
df_border['lat'] = df_border['lat'].apply(lambda x: listrize(x))
df_emergency_route['lon'] = df_emergency_route['lon'].apply(lambda x: listrize(x))
df_emergency_route['lat'] = df_emergency_route['lat'].apply(lambda x: listrize(x))


# In[ ]:


def num_b_r(d_num):
    return d_num['num_bikes_rentalable']

df_hellowcycle['num_bikes_rentalable'] = df_hellowcycle['vehicle_type_capacity'].apply(
    lambda x: num_b_r(x))


# In[ ]:


def violin_general(df):
    fig=go.Figure()
    df_fe = df.drop(columns=['Pop_male', 'Pop_female', 'Household', '0_4_m', '5_9_m', '10_14_m', '15_19_m', '20_24_m', '25_29_m', '30_34_m', 
                             '35_39_m', '40_44_m', 
                            '45_49_m', '50_54_m', '55_59_m', '60_64_m', '65_69_m', '70_74_m', '75_79_m', '80_84_m', '85_89_m', '90_94_m', '95_99_m'])
    
    
    df_m = df.drop(columns=['Pop_male', 'Pop_female', 'Household', '0_4_f', '5_9_f', '10_14_f', '15_19_f', '20_24_f', '25_29_f', '30_34_f', 
                             '35_39_f', '40_44_f', 
                            '45_49_f', '50_54_f', '55_59_f', '60_64_f', '65_69_f', '70_74_f', '75_79_f', '80_84_f', '85_89_f', '90_94_f', '95_99_f'])
    
    df_fe.set_index('Year', inplace=True)
    df_m.set_index('Year', inplace=True)
    
    violin_tickval = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',
                                                      '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90-94', '95-99']
    
    tf_list = []
    
    for y in df['Year'].unique():
        
        tf = [False]*2*len(df['Year'].unique())
        
        i = list(df['Year'].unique()).index(y)
        tf[2*i] = True
        tf[2*i+1] = True
        tf_list.append(tf)
    
        fig.add_trace(go.Violin(y=df_m.loc[y],
                        legendgroup='Male', scalegroup='Male', name='{} Male'.format(y),
                        side='negative',
                        line_color='lightseagreen', showlegend=False, hovertext='{} Male'.format(y), x0=0))
        fig.add_trace(go.Violin(y=df_fe.loc[y],
                        legendgroup='Female', scalegroup='Female', name='{} Female'.format(y),
                        side='positive',
                        line_color='coral', showlegend=False, hovertext='{} Female'.format(y), x0=0))
        fig.update_layout(violinmode='overlay')
                      
    dict_list = []
    
    for i in range(len(list(df['Year'].unique()))):
        dict_list.append(dict(
        label="{}".format(list(df['Year'].unique())[i]),
        method="update",
        args=[{"visible": tf_list[i]},
        {"title": "<b>Distribution of Population across age (0-99) {}</b>".format(df['Year'].unique()[i]),
        'font': {'family': font_fam_sp}}]))
    
    fig.update_layout(paper_bgcolor="#d9e3f1",
                      title='<b>Choose a year</b>',
                      title_font={'family':font_fam_sp},
                      width=700,
                      height=400,
        updatemenus=[
            dict(
                active=0,
                buttons=list(dict_list),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.2,
                yanchor="top")
        ])
                      
    fig.update_traces(meanline_visible=True)
    fig.update_yaxes(title_text='Age Group', tickvals=violin_tickval, title_font={'family':font_fam_sp})
    
    return fig


# In[ ]:


def population_general(df):
    fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    specs=[[{"type": "scatter"}, {"type": "xy", 'secondary_y':True}]],
           )
    
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Pop_male'], name='Male Population', showlegend=True, hovertext='Male Population'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Pop_female'], name='Female Population', showlegend=True, hovertext='Female Population')
                  , row=1, col=1)
    fig.update_xaxes(title_text='Year', tickvals=list(df['Year'].unique()), row=1, col=1, title_font={'family':font_fam_sp})
    fig.update_yaxes(title_text='Population', row=1, col=1, title_font={'family':font_fam_sp})
    
    fig.add_trace(go.Bar(x=df['Year'], y=df['Household'], name='Number of Household', showlegend=True, hovertext='Number of Household')
                  , secondary_y=False, row=1, col=2)
    fig.add_trace(go.Scatter(x=df['Year'], y=(df['Pop_male']+df['Pop_female'])/df['Household'], name='Number per a Household', 
                    hovertext='Number per a Household', showlegend=False), secondary_y=True, 
                  row=1, col=2)
    
    fig.update_yaxes(title_text="Number per a Household", secondary_y=True, row=1, col=2, title_font={'family':font_fam_sp})
    fig.update_yaxes(title_text="Number of Household", secondary_y=False, row=1, col=2, title_font={'family':font_fam_sp})
    fig.update_xaxes(title_text='Year', row=1, col=2)
    fig.update_layout(paper_bgcolor="#d9e3f1", height=400, width=1000, legend={"itemsizing": "constant"})
    
    return fig


# In[ ]:


token = open("assets/token_mapbox.txt").read()

symbol_type = {'病院':{'symbol':'hospital', 'color':'crimson'},
                   '消防署':{'symbol':'fire-station', 'color':'red'},
                   '警察署':{'symbol':'police', 'color':'indianred'},
                   '郵便局':{'symbol':'post', 'color':'tomato'},
                   '保健所':{'symbol':'blood-bank', 'color':'firebrick'},
                   '国の機関':{'symbol':'embassy', 'color':'blue'},
                   '地方の機関':{'symbol':'town-hall', 'color':'royalblue'},
                   '指定公共機関':{'symbol':'place-of-worship', 'color':'midnightblue'},
                   '博物館・美術館':{'symbol':'museum', 'color':'brown'},
                   '学校':{'symbol':'college', 'color':'navy'},
                   'ランドマーク':{'symbol':'castle', 'color':'black'}
              }

def type_symbol_conversion(types):
    return symbol_type[types]['symbol']

def type_color_conversion(types):
    return symbol_type[types]['color']

def sizeconversion(volume, max_, min_):
    if volume==0:
        return 10
    else:
        return 10 + 30*((volume-min_)/(max_-min_))
    

df_landmark['symbol'] = df_landmark['種類'].apply(lambda x: type_symbol_conversion(x))
df_landmark['color'] = df_landmark['種類'].apply(lambda x: type_color_conversion(x))
df_shelter['size'] = df_shelter['収容人数'].apply(
        lambda x: sizeconversion(x, df_shelter['収容人数'].max(), df_shelter['収容人数'].min()))
df_park['size'] = df_park['供用済面積'].apply(
        lambda x: sizeconversion(x, df_park['供用済面積'].max(), df_park['供用済面積'].min()))
df_hellowcycle['size'] = df_hellowcycle['num_bikes_rentalable'].apply(
        lambda x: sizeconversion(x, df_hellowcycle['num_bikes_rentalable'].max(), df_hellowcycle['num_bikes_rentalable'].min()))
df_docomo['size'] = df_docomo['capacity'].apply(lambda x: sizeconversion(x, df_docomo['capacity'].max(), df_docomo['capacity'].min()))


# In[ ]:


layout = dbc.Container([
                html.Br(),
                html.Div(html.H1('CITY', className="display-2", 
                        style={'textAlign':'left', 'color':'midnightblue', 'font-size':30})
                        ),
                html.Div('西東京市の都市・人口情報を見る。ほかの自治体の都市・人口情報を可視化する。', 
                style={'font-family':'游明朝', 'textAlign':'left', 'color':'royalblue', 'font-size':20}
                                      , className="fw-light"),
                html.Br(),
                html.Br(),
                html.Div(
            [
               dbc.Button(
                    "ABOUT",
                    id="about-offcanvas-scrollable_map",
                   n_clicks=0,
               ),
               dbc.Offcanvas(
                    [html.Hr(), html.P(
                    "A resource for knowing, learning about and\ngetting excited about a city,\ndesigned mainly for Nishi Tokyo City, Tokyo,\nbut can be applied to any other city."
                    ),
                     html.P("-Map visualization of facilities in Nishi Tokyo"), 
                     html.P("-Uploading your city's PLATEAU data and getting a map out"), html.Br(),
                    dcc.Markdown('''
                    **Contact : westt.sskry(at)gmail.com**
                    ''')],
                    id="offcanvas-scrollable_map",
                    scrollable=True,
                    title="About this page",
                    is_open=False,
                      ),
           ]
        ),
             html.Br(),
             html.Br(),            
             html.Div([html.H2('Basic Statistical Figures', 
                               style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
                  dbc.Button('?', outline=True, color='info', style={'textAlign': 'center', 'font-size': 15}, n_clicks=0, id='doc_button1_map')
                 ]),
             html.Div(dbc.Collapse(
                 dbc.Card([dbc.CardHeader('GRAPH DESCRIPTION'),
                 dbc.CardBody([
                 html.P( 
                 dcc.Markdown('''
            *POPULATION*: The trend of population and its distribution across age (0-99) of Nishi Tokyo 2003-2023. 
                          The value for 2003 is that of Jan 1st 2004. Other years have value of Dec 1st of that year.
            ''')), html.P([html.B('Source'), html.Div(dcc.Markdown('''
            https://www.city.nishitokyo.lg.jp/siseizyoho/tokei/zinko/index.html
            
            '''))])])],
            color='info', outline = True),
            id='doc1_map',
            is_open=False,
        )),
        html.Hr(),
        html.Br(),
        html.Br(),
        html.Div(dbc.Tabs(
        dbc.Tab(label='POPULATION', children=[html.Br(),
            dbc.Spinner(
                dcc.Graph(
                figure=population_general(df_pop)), color='dark'),
            dbc.Spinner(
                dcc.Graph(figure=violin_general(df_pop)), color='dark')
        ]),
    )
    ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([html.H2('City Features', 
                               style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
                  dbc.Button('?', outline=True, color='info', 
                             style={'textAlign': 'center', 'font-size': 15}, n_clicks=0, id='doc_button2_map')
                 ]),
             html.Div(dbc.Collapse(
                      dbc.Card([dbc.CardHeader('MAP DESCRIPTION'),
                      dbc.CardBody([
             html.P( 
                      dcc.Markdown('''
            *LANDMARK*: Provided by PLATEAU
            
            *STATION*: Provided by PLATEAU
            
            *EMERGENCY ROUTE*: Provided by PLATEAU
            
            *SHELTER*: Icon size has a correlation with its capacity. Provided by PLATEAU
            
            *PARK*: Provided by PLATEAU
            
            *BORDER*: Provided by PLATEAU
            
            *SHARE CYCLE STATION*: Icon size has a correlation with its rentalable bike number. Provided by ODPT
            ''')), html.P([html.B('Source'), 
            dcc.Markdown('''
            https://www.geospatial.jp/ckan/dataset/plateau-13229-nishitokyo-shi-2022/resource/d6d01b02-9c53-46c9-99c7-0a4f75da34dd
            
            https://www.odpt.org/2022/06/28/press20220628_bikeshare/
            ''')])])],
            color='info', outline = True),
            id='doc2_map',
            is_open=False,
        )),
             html.Hr(),
             html.Br(),
             html.Br(),
             html.Div(dbc.Spinner(dcc.Graph(id='map_'), color='dark')
                      , style={'position':'relative', 'left':150}),
             html.Br(),
             html.Br(),
             html.Div([dbc.Card(
                 dbc.CardBody(dbc.Col([
                     dbc.Row(html.H4('SET VALUES', className="card-title", style={'color':'white'})),
                     dbc.Row(children=
                     [dcc.Markdown('''Choose Attributes''', style={'color':'white'}), 
                       dcc.Checklist(['LANDMARK', 'STATION', 'EMERGENCY ROUTE', 'SHELTER', 'PARK', 
                                      'BORDER', 'SHARE CYCLE STATION'], 
                                     id='attributes_map', inline=True,
                  style = {'display': 'flex', 'color':'white'}
                 )])
                ])
            ), color='info')
        ]),
    html.Div(dbc.Button(id='submit-button-state1_map', n_clicks=0, children='Select Values', color='info')),
    html.Br(),
    html.Div(id='selection_completed_map'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('Make figures of your city!', style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
             dbc.Button('?', outline=True, color='info', 
                        style={'textAlign': 'center', 'font-size': 15, 'className':'mb-3'}, n_clicks=0, id='doc_button3_map')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('DESCRIPTION'),
            dbc.CardBody([html.P(dcc.Markdown('''
            By uploading CSV or GeoJSON files, you can obtain figures. File format restriction is strict. 
            Please see below for the info.
            '''))])],
            color='info', outline = True),
            id='doc3_map',
            is_open=False,
        )),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.H3('Basic Statistical Figures', style={'textAlign': 'left', 'color': '#503D36', 'font-size': 20}),
    html.Div(
    dcc.Upload(
        id='upload-data_pop',
        children=html.Div(['Drag and Drop or ',html.A('Select a CSV File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    )),
    html.H3('Your Graphs:', style={'font-size':20}),
    html.Br(),
    html.Div(id='output-data-upload_pop'),
    html.Br(),
    html.H3('City Features', style={'textAlign': 'left', 'color': '#503D36', 'font-size': 20}),
    html.Div([
    dcc.Upload(
        id='upload-data_landmark',
        children=html.Div(['Drag and Drop or ',html.A('Select a GeoJSON File'), 'that contains LANDMARK info'
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    dcc.Upload(
        id='upload-data_station',
        children=html.Div(['Drag and Drop or ',html.A('Select a GeoJSON File'), 'that contains STATION info'
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    dcc.Upload(
        id='upload-data_emergency_route',
        children=html.Div(['Drag and Drop or ',html.A('Select a GeoJSON File'), 'that contains EMERGENCY ROUTE info'
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    dcc.Upload(
        id='upload-data_shelter',
        children=html.Div(['Drag and Drop or ',html.A('Select a GeoJSON File'), 'that contains SHELTER info'
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    dcc.Upload(
        id='upload-data_park',
        children=html.Div(['Drag and Drop or ',html.A('Select a GeoJSON File'), 'that contains PARK info'
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    dcc.Upload(
        id='upload-data_border',
        children=html.Div(['Drag and Drop or ',html.A('Select a GeoJSON File'), 'that contains BORDER info'
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        style_active={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '5px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    )]),
    html.Div(dbc.Button('SUBMIT FILES (Be sure all of the 6 forms are filled)', color='info', n_clicks=0, id='submit_upload_map1')),
    html.Br(),
    html.H3('Your Map:', style={'font-size':20}),
    html.Br(),
    html.Div(id='output-data-upload_map1', style={'position':'relative', 'left':150}),
    html.Br(),
    html.Br(),
    html.H3('File Format'),
    html.Br(),
    html.Div(
    dbc.Accordion([
        dbc.AccordionItem(
        [html.P([html.B('File Type'), html.Div('-CSV')]), html.P([html.B('Encoding'), html.Div('-Shift JIS')]),
        html.P([html.B('Columns'), dcc.Markdown('''
        *-Year* (Year)
        
        *-Pop_male* (Total population of male)
        
        *-Pop_femal* (Total population of female)
        
        *-Household* (Number of households)
        
        *-0_4_m, 5_9_m, ..., 95_99_m* (Population of each age group (0 years old to 4 years old, and so on), male)
        
        *-0_4_f, 5_9_f, ..., 95_99_f* (Population of each age group (0 years old to 4 years old, and so on), female)
        
        ''')]),
        html.P([html.B('Note'), html.Div('-No empty cell accepted')])], title='Basic Statistical Figures'),
            dbc.AccordionItem(
                [html.P([html.B("File Type"),html.Div("-GeoJSON")]), html.P([html.B("Encoding"), html.Div("-UTF-8")]), 
                 html.P([html.B("Formats"),dcc.Markdown('''
                 **PLATEAU open data GeoJSON files are the expected inputs here. Please see: https://www.mlit.go.jp/plateau/open-data/**
                 
                *-Landmark* (Longitude, Latitude, Type, Name)
                
                *-Station* (Longitude, Latitude, Name)
                
                *-Emergency Route* (Linestring, Name)
                
                *-Shelter* (Longitude, Latitude, Capacity, Name)
                
                *-Park* (Longitude, Latitude, Area, Name)
                
                *-Border* (City Border, Your map's center is located based on this file)
                 ''')]),
                html.P([html.B("Note"), html.Div("-Columns which have nulls (NaNs, N/As) are replaced with 0 automatically")])]
                , title="City Features"
            ),],
                 flush=True,
                 start_collapsed=True,
             ),
        ),
    html.Br(),
    html.Br(),
    html.Br(),

    dbc.NavbarSimple(
        dbc.NavItem(
            dbc.Row([
                dbc.Col(html.Img(src='assets/github_mark.png', height='15',
                                 style={'position': 'relative', 'top': '16%', 'left': '80%'})),
                dbc.Col(
                    dbc.NavLink('Github',
                                href='https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-',
                                style={'font-size': '1.5vh', 'textAlign': 'center', 'color': 'navy'}))
            ])
        ),
        brand='This page uses Dash, is themed by Bootstrap.Morph, and is deployed by Render.',
        dark=True,
        brand_style={'font-size': '1.5vh', 'textAlign': 'center', 'color': 'navy',
                     'font': 'italic 1.2rem "Fira Sans", serif'},
        color='info',
        sticky='bottom',
        style={'height': '3vh', 'width':'100vw'},
    ), style={'overflow-x':'hidden'}

])


# In[ ]:


@callback(
    Output("upload-data_landmark", "style"),
    Input("upload-data_landmark", "contents")
)
def hide_upload_l(contents):
    if contents is not None:
        return {"display": "none"}
    return dash.no_update

@callback(
    Output("upload-data_station", "style"),
    Input("upload-data_station", "contents")
)
def hide_upload_sta(contents):
    if contents is not None:
        return {"display": "none"}
    return dash.no_update

@callback(
    Output("upload-data_emergency_route", "style"),
    Input("upload-data_emergency_route", "contents")
)
def hide_upload_er(contents):
    if contents is not None:
        return {"display": "none"}
    return dash.no_update

@callback(
    Output("upload-data_shelter", "style"),
    Input("upload-data_shelter", "contents")
)
def hide_upload_sh(contents):
    if contents is not None:
        return {"display": "none"}
    return dash.no_update

@callback(
    Output("upload-data_park", "style"),
    Input("upload-data_park", "contents")
)
def hide_upload_pa(contents):
    if contents is not None:
        return {"display": "none"}
    return dash.no_update

@callback(
    Output("upload-data_border", "style"),
    Input("upload-data_border", "contents")
)
def hide_upload_bo(contents):
    if contents is not None:
        return {"display": "none"}
    return dash.no_update

def parse_content_pop(content, filename):
    content_type, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df_in = pd.read_csv(
                io.StringIO(decoded.decode('shift-jis')))
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div(dbc.Tabs(dbc.Tab(label='POPULATION', children=[html.Br(),
            dcc.Graph(
                figure=population_general(df_in)),
            dcc.Graph(figure=violin_general(df_in))
        ]),))
    
@callback(
          Output('output-data-upload_pop', 'children'),
               Input('upload-data_pop', 'contents'),
               State('upload-data_pop', 'filename')
             )

def update_output_pop(content, name):
    if content is not None:
        children = [parse_content_pop(content, name)]
        return children
    
    
def parse_content_markers(content, filename):
    content_type, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'geojson' in filename:
            # Assume that the user uploaded a CSV file
            df_in = gpd.read_file(
                io.StringIO(decoded.decode('utf-8')))
            
            df_in['lon'] = df_in['geometry'].apply(lambda geom: geom.x if geom else None)
            df_in['lat'] = df_in['geometry'].apply(lambda geom: geom.y if geom else None)
            df_in.drop(columns=['geometry'], inplace=True)
            
    except Exception as e:
        print(e)
        return None
    return df_in

def extract_coordinates(geometry):
    if geometry:
        lon, lat = geometry.xy
        return list(zip(lon, lat))
    else:
        return None
    
def extract_lon(lon_lat):
    lon_ln = []
    for i in range(len(lon_lat)):
        lon_ln.append(lon_lat[i][0])
        
    return lon_ln

def extract_lat(lon_lat):
    lat_ln = []
    for i in range(len(lon_lat)):
        lat_ln.append(lon_lat[i][1])
        
    return lat_ln

def parse_content_lines(content, filename):
    content_type, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'geojson' in filename:
            df_in = gpd.read_file(
                io.StringIO(decoded.decode('utf-8')))
            
            geometry_type = df_in['geometry'].geom_type.unique()[0]
            
            if geometry_type == 'LineString':
                df_in = df_in.set_geometry('geometry').explode(index_parts=True).reset_index(drop=True)
                df_in['lon_lat'] = df_in['geometry'].apply(extract_coordinates)
                df_in['lon'] = df_in['lon_lat'].apply(lambda x: extract_lon(x))
                df_in['lat'] = df_in['lon_lat'].apply(lambda x: extract_lat(x))
                df_in.drop(columns=['geometry'], inplace=True)
                
            elif geometry_type == 'MultiPolygon':
                df_in = df_in.set_geometry('geometry').explode(index_parts=True).reset_index(drop=True)
                df_in['lon'] = df_in['geometry'].apply(lambda geom: list(geom.exterior.coords.xy[0]) if geom else [])
                df_in['lat'] = df_in['geometry'].apply(lambda geom: list(geom.exterior.coords.xy[1]) if geom else [])
                df_in.drop(columns=['geometry'], inplace=True)
                
            elif geometry_type == 'Polygon':
                df_in = df_in.set_geometry('geometry').explode(index_parts=True).reset_index(drop=True)
                df_in['lon'] = df_in['geometry'].apply(lambda geom: list(geom.exterior.coords.xy[0]) if geom else [])
                df_in['lat'] = df_in['geometry'].apply(lambda geom: list(geom.exterior.coords.xy[1]) if geom else [])
                df_in.drop(columns=['geometry'], inplace=True)

            elif geometry_type == 'MultiLineString':
                df_in = df_in.set_geometry('geometry').explode(index_parts=True).reset_index(drop=True)
                df_in['lon'] = df_in['geometry'].apply(lambda geom: list(geom.coords.xy[0]) if geom else [])
                df_in['lat'] = df_in['geometry'].apply(lambda geom: list(geom.coords.xy[1]) if geom else [])
                df_in.drop(columns=['geometry'], inplace=True)
                
    except Exception as e:
        print(e)
        return None
    return df_in

@callback(Output('output-data-upload_map1', 'children'),
          State('upload-data_landmark', 'contents'),
          State('upload-data_landmark', 'filename'),
          State('upload-data_station', 'contents'),
          State('upload-data_station', 'filename'),
          State('upload-data_emergency_route', 'contents'),
          State('upload-data_emergency_route', 'filename'),
          State('upload-data_shelter', 'contents'),
          State('upload-data_shelter', 'filename'),
          State('upload-data_park', 'contents'),
          State('upload-data_park', 'filename'),
          State('upload-data_border', 'contents'),
          State('upload-data_border', 'filename'),
          Input('submit_upload_map1', 'n_clicks'))

def return_a_map(c_land, f_land, c_sta, f_sta, c_er, f_er, c_sh, f_sh, c_pa, f_pa, c_bo, f_bo, n):
    if n%2 == 0:
        raise PreventUpdate
        
    if n%2 == 1:
        try:
            df_l = parse_content_markers(c_land, f_land)
            df_sta = parse_content_markers(c_sta, f_sta)
            df_er = parse_content_lines(c_er, f_er)
            df_sh = parse_content_markers(c_sh, f_sh)
            df_pa = parse_content_markers(c_pa, f_pa)
            df_bo = parse_content_lines(c_bo, f_bo)
        
            df_bo['lon'] = df_bo['lon'].apply(lambda x: listrize(x))
            df_bo['lat'] = df_bo['lat'].apply(lambda x: listrize(x))
            df_er['lon'] = df_er['lon'].apply(lambda x: listrize(x))
            df_er['lat'] = df_er['lat'].apply(lambda x: listrize(x))
        
            df_l['symbol'] = df_l['種類'].apply(lambda x: type_symbol_conversion(x))
            df_l['color'] = df_l['種類'].apply(lambda x: type_color_conversion(x))

            if '収容人数' in df_sh.columns:
                df_sh['収容人数'] = df_sh['収容人数'].fillna(0)
                df_sh['収容人数'] = df_sh['収容人数'].astype(float)
                df_sh['size'] = df_sh['収容人数'].apply(
                lambda x: sizeconversion(x, df_sh['収容人数'].max(), df_sh['収容人数'].min()))
                
            else:
                df_sh['size'] = 10
                
            if '供用済面積' in df_pa.columns:
                df_pa['供用済面積'] = df_pa['供用済面積'].fillna(0)
                df_pa['供用済面積'] = df_pa['供用済面積'].astype(float)
                df_pa['size'] = df_pa['供用済面積'].apply(
                lambda x: sizeconversion(x, df_pa['供用済面積'].max(), df_pa['供用済面積'].min()))
                
            else:
                df_pa['size'] = 10
        
            fig = go.Figure()
    
            alat = []
            alon = []
            
            for k in range(len(df_bo['lat'])):
    
                alat.append(sum(df_bo['lat'][k]) / len(df_bo['lat'][k]))
                alon.append(sum(df_bo['lon'][k]) / len(df_bo['lon'][k]))
            
            avg_lat=sum(alat)/len(alat)
            avg_lon=sum(alon)/len(alon)
    
            fig.add_trace(go.Scattermapbox(
            lat=list(df_l['lat']),
            lon=list(df_l['lon']),
            mode='markers',
            marker={'size': 15, 'symbol': list(df_l['symbol']), 'color': list(df_l['color'])},
            text=list(df_l['名称']),
            hoverinfo=['text', 'name'],
            name='LANDMARK',
            textfont={'family':font_fam_sp}
        ))
    
            fig.add_trace(go.Scattermapbox(
            lat=list(df_sta['lat']),
            lon=list(df_sta['lon']),
            mode='markers',
            marker={'size': 15, 'symbol': 'rail', 'color': 'purple'},
            text=list(df_sta['駅名']),
            hoverinfo=['text', 'name'],
            name='STATION',
            textfont={'family':font_fam_sp}
        ))
    
            for i in range(len(df_er['lat'])):
    
                fig.add_trace(go.Scattermapbox(
            lat=df_er['lat'][i],
            lon=df_er['lon'][i],
            mode='lines',
            line={'color':'violet', 'width':3},
            text=df_er['路線名称'][i],
            hoverinfo=['text', 'name'],
            name='EMERGENCY ROUTE',
            textfont={'family':font_fam_sp}
        ))
        
            fig.add_trace(go.Scattermapbox(
        lat=list(df_sh['lat']),
        lon=list(df_sh['lon']),
        mode='markers',
        marker={'size': list(df_sh['size']), 'symbol': 'lodging', 'color': 'deeppink'},
        text=list(df_sh['名称']),
        hoverinfo=['text', 'name'],
        name='SHELTER',
        textfont={'family':font_fam_sp}
    ))
    
            fig.add_trace(go.Scattermapbox(
        lat=list(df_pa['lat']),
        lon=list(df_pa['lon']),
        mode='markers',
        marker={'size': list(df_pa['size']), 'symbol': 'park', 'color': 'lightgreen'},
        text=list(df_pa['公園名']),
        hoverinfo=['text', 'name'],
        name='PARK',
        textfont={'family':font_fam_sp}
    ))
    
            for j in range(len(df_bo['lat'])):
                fig.add_trace(go.Scattermapbox(
        lat=df_bo['lat'][j],
        lon=df_bo['lon'][j],
        mode='lines',
        line={'color':'orangered', 'width':7},
        hoverinfo=['name'],
        name='境界線',
        textfont={'family':font_fam_sp}
    ))
    
            fig.add_trace(go.Scattermapbox(
        lat=list(df_hellowcycle['lat']),
        lon=list(df_hellowcycle['lon']),
        mode='markers',
        marker={'size': list(df_hellowcycle['size']), 'symbol':'bicycle-share', 'color':'black'},
        hoverinfo=['text', 'name'],
        hovertext=list(df_hellowcycle['parking_type']),
        name='ハローサイクリング',
        textfont={'family':font_fam_sp}
    ))
    
            fig.add_trace(go.Scattermapbox(
        lat=list(df_docomo['lat']),
        lon=list(df_docomo['lon']),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=list(df_docomo['size']), symbol='bicycle-share', color='black'),
        text=list(df_docomo['capacity']),
        hoverinfo=['text', 'name'],
        name='docomo',
        textfont={'family':font_fam_sp}
    ))

            fig.update_layout(autosize=False,
                      height=600,
                      width=800,
                      mapbox = {
        'accesstoken': token,
        'style': "basic", 'zoom': 12,
         'center':dict(
            lat=avg_lat,
            lon=avg_lon
        )},
        showlegend = False, paper_bgcolor = '#d9e3f1')
    
        except Exception as e:
            print(e)
            return [html.Div('There was an error processing files.')]
        
        return [html.Div(dbc.Spinner(dcc.Graph(figure=fig)), color='dark')]

@callback(
    Output("doc2_map", "is_open"),
    Input("doc_button2_map", "n_clicks"),
    State("doc2_map", "is_open"),
)
def toggle_collapse2_map(n, is_open):
    if n:
        return not is_open
    return is_open

def map_drawing(values_ln):
    fig = go.Figure()
    
    avg_lat = sum(df_border['lat'][0]) / len(df_border['lat'][0])
    avg_lon = sum(df_border['lon'][0]) / len(df_border['lon'][0])
    
    trace_landmark = go.Scattermapbox(
        lat=list(df_landmark['lat']),
        lon=list(df_landmark['lon']),
        mode='markers',
        marker={'size': 15, 'symbol': list(df_landmark['symbol']), 'color': list(df_landmark['color'])},
        hovertext=list(df_landmark['名称']),
        hoverinfo=['text', 'name'],
        name='LANDMARK',
        textfont={'family':font_fam_sp}
    )
    
    trace_station = go.Scattermapbox(
        lat=list(df_station['lat']),
        lon=list(df_station['lon']),
        mode='markers',
        marker={'size': 15, 'symbol': 'rail', 'color': 'purple'},
        hovertext=list(df_station['駅名']),
        hoverinfo=['text', 'name'],
        name='STATION',
        textfont={'family':font_fam_sp}
    )
    
    trace_emergency_route = []
    for i in range(len(df_emergency_route['lat'])):
    
        trace_ = go.Scattermapbox(
            lat=df_emergency_route['lat'][i],
            lon=df_emergency_route['lon'][i],
            mode='lines',
            line={'color':'violet', 'width':5},
            hovertext=df_emergency_route['路線名称'][i],
            hoverinfo=['text', 'name'],
            name='EMERGENCY ROUTE',
            textfont={'family':font_fam_sp}
        )
        
        trace_emergency_route.append(trace_)
    
    trace_shelter = go.Scattermapbox(
        lat=list(df_shelter['lat']),
        lon=list(df_shelter['lon']),
        mode='markers',
        marker={'size': list(df_shelter['size']), 'symbol': 'lodging', 'color': 'deeppink'},
        hovertext=list(df_shelter['名称']),
        hoverinfo=['text', 'name'],
        name='SHELTER',
        textfont={'family':font_fam_sp}
    )
    
    trace_park = go.Scattermapbox(
        lat=list(df_park['lat']),
        lon=list(df_park['lon']),
        mode='markers',
        marker={'size': list(df_park['size']), 'symbol': 'park', 'color': 'lightgreen'},
        hovertext=list(df_park['公園名']),
        hoverinfo=['text', 'name'],
        name='PARK',
        textfont={'family':font_fam_sp}
    )
    
    trace_border = go.Scattermapbox(
        lat=df_border['lat'][0],
        lon=df_border['lon'][0],
        mode='lines',
        line={'color':'orangered', 'width':10},
        hoverinfo=['name'],
        name='境界線',
        textfont={'family':font_fam_sp}
    )
    
    trace_hellowcycle = go.Scattermapbox(
        lat=list(df_hellowcycle['lat']),
        lon=list(df_hellowcycle['lon']),
        mode='markers',
        marker={'size': list(df_hellowcycle['size']), 'symbol':'bicycle-share', 'color':'black'},
        hoverinfo=['text', 'name'],
        hovertext=list(df_hellowcycle['parking_type']),
        name='ハローサイクリング',
        textfont={'family':font_fam_sp}
    )
    
    trace_docomo = go.Scattermapbox(
        lat=list(df_docomo['lat']),
        lon=list(df_docomo['lon']),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=list(df_docomo['size']), symbol='bicycle-share', color='black'),
        text=list(df_docomo['capacity']),
        hoverinfo=['text', 'name'],
        name='docomo share cycle',
        textfont={'family':font_fam_sp}
    )
    
    traces = [trace_landmark, trace_station, trace_emergency_route, trace_shelter, trace_park, trace_border, 
              trace_hellowcycle, trace_docomo]
    
    fig.add_trace(go.Scattermapbox())
    
    fig.update_layout(autosize=False,
                      height=600,
                      width=800,
                      mapbox = {
        'accesstoken': token,
        'style': "basic", 'zoom': 12,
         'center':dict(
            lat=avg_lat,
            lon=avg_lon
        )},
        showlegend = False, paper_bgcolor = '#d9e3f1')
    
    if len(values_ln) != 0:
        for i in values_ln:
            if i != 2:
                fig.add_trace(traces[i])
                
            if i == 2:
                for j in range(len(traces[i])):
                    fig.add_trace(traces[i][j])
            
    return fig


@callback(Output('map_', 'figure'),
         Input('submit-button-state1_map', 'n_clicks'),
         State('attributes_map', 'value'),
         id='map_at')

def map_display(n, values):
    full_value = ['LANDMARK', 'STATION', 'EMERGENCY ROUTE', 'SHELTER', 'PARK', 'BORDER', 'SHARE CYCLE STATION']
    values_ln = []
    if n%2 == 1:
        if values == None:
            return map_drawing([])
    
        else:
            if not isinstance(values, list):
                values = [values]
                
            for x in values:
                if x in full_value:
                    values_ln.append(full_value.index(x))
                    
            if 6 in values_ln:
                values_ln.append(7)
                
            return map_drawing(values_ln)
    else:
        raise PreventUpdate

@callback(
    Output("offcanvas-scrollable_map", "is_open"),
    Input("about-offcanvas-scrollable_map", "n_clicks"),
    State("offcanvas-scrollable_map", "is_open"),
)
def toggle_offcanvas_scrollable_map(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(
    Output("doc1_map", "is_open"),
    Input("doc_button1_map", "n_clicks"),
    State("doc1_map", "is_open"),
)
def toggle_collapse1_map(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("doc3_map", "is_open"),
    Input("doc_button3_map", "n_clicks"),
    State("doc3_map", "is_open"),
)
def toggle_collapse3_map(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(Output('selection_completed_map', 'children'),
         Input('submit-button-state1_map', 'n_clicks'))

def completion_alert_map(n_clicks):
    if n_clicks%2 == 1:
        return [dbc.Alert("Submitted!!! (Press the button again before changing values again)", color="secondary")]
    
    else:
        return [dbc.Alert("Please select values and press submit button", color="info")]

