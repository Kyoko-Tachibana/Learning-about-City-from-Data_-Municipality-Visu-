#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import ast
import plotly
import plotly.express as px
import dash
from dash import html
from dash import dcc
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import nlplot
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import base64
import io
from dash import callback, State
from dash import callback, State
from dash.dependencies import Input, Output
import dash_daq as daq
from plotly.colors import n_colors
from plotly.subplots import make_subplots
from dash import Dash
from itertools import compress
import math
import dash_bootstrap_components as dbc

df=pd.read_csv('assets/Data_NishiTokyo_CityCouncil.csv', encoding='shift-jis')
df_table=pd.read_csv('assets/Data_NishiTokyo_CityCouncil_fortable.csv', encoding='shift-jis')
df_vote_rate = pd.read_csv('assets/Vote_rate.csv')
df_table_city = df_table[df_table['Type']=='市議']

df_filtered_list = []
for y in range(2001, 2023):
    df_f = pd.read_csv('assets/{} filtered.csv'.format(y), encoding='shift-jis')
    df_f.dropna(subset=['selectednouns'], inplace=True)
    df_f['selectednouns'] = df_f['selectednouns'].apply(ast.literal_eval)
    df_filtered_list.append(df_f)

def candidate_info(df):
    fig = go.Figure()
    colors = n_colors('rgb(197, 216, 255)', 'rgb(253, 222, 250)', 2, colortype='rgb')
    for year in df[df['Type']=='市議']['Year'].unique():
        df_y = df[(df['Year']==year)&(df['Type']=='市議')]

        columnorder = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        columnwidth = [1.5, 1.1, 1, 1, 3.2, 3.2, 3, 3.2, 3, 1.2, 1.2, 1.8, 1.8]
        
        fig.add_trace(go.Table(columnorder=columnorder, columnwidth=columnwidth, name='Candidates of {} city council election'.format(year),
        header=dict(values=[['<b>NAME</b>'], ['<b>PARTY</b>'], ['<b>AGE</b>'], ['<b>SEX</b>'], ['<b>CAREER</b>'], 
                ['<b>EDUCATIONAL</b><br><b>PLEDGE</b>'], ['<b>WELFARE</b><br><b>PLEDGE</b>'], 
                ['<b>CITYPLANNING</b><br><b>PLEDGE</b>'], ['<b>OTHER</b><br><b>PLEDGE</b>'], ['<b>VOTES<br></b>'], 
                ['<b>VOTES<br></b>(%)'], ['<b>PREVIOUS<br>VOTES<br></b>'], ['<b>PREVIOUS<br>VOTES<br></b>(%)']],
                fill_color='paleturquoise',
                align='left',
                font_size=10),
        cells=dict(values=[df_y.Candidate, df_y.Party, df_y.Age, df_y.Sex, df_y.Career, df_y.edu, df_y.wel, df_y.city, df_y.other, 
                           df_y.Vote_num, df_y.Vote, df_y.Vote_num_p, df_y.Vote_p],
               fill_color=[np.array(colors)[list(map(int, df_y.Result))]]*13,
               align='left',
               font=dict(color='black', size=9))))

    for year in df[df['Type']=='市長']['Year'].unique():
        df_y_mayor = df[(df['Year']==year)&(df['Type']=='市長')]

        columnorder = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        columnwidth = [1.5, 1.1, 1, 1, 3.2, 3.2, 3, 3.2, 3, 1.2, 1.2, 1.8, 1.8]
        
        fig.add_trace(go.Table(columnorder=columnorder, columnwidth=columnwidth, name='Candidates of {} mayor election'.format(year),
        header=dict(values=[['<b>NAME</b>'], ['<b>PARTY</b>'], ['<b>AGE</b>'], ['<b>SEX</b>'], ['<b>CAREER</b>'], 
                ['<b>EDUCATIONAL</b><br><b>PLEDGE</b>'], ['<b>WELFARE</b><br><b>PLEDGE</b>'], 
                ['<b>CITYPLANNING</b><br><b>PLEDGE</b>'], ['<b>OTHER</b><br><b>PLEDGE</b>'], ['<b>VOTES<br></b>'], 
                ['<b>VOTES<br></b>(%)'], ['<b>PREVIOUS<br>VOTES</b>'], ['<b>PREVIOUS<br>VOTES</b><br>(%)']],
                fill_color='paleturquoise',
                align='left',
                font_size=10),
        cells=dict(values=[df_y_mayor.Candidate, df_y_mayor.Party, df_y_mayor.Age, df_y_mayor.Sex, df_y_mayor.Career, df_y_mayor.edu, df_y_mayor.wel, 
                           df_y_mayor.city, df_y_mayor.other, df_y_mayor.Vote_num, df_y_mayor.Vote, df_y_mayor.Vote_num_p, 
                           df_y_mayor.Vote_p],
               fill_color=[np.array(colors)[list(map(int, df_y_mayor.Result))]]*13,
               align='left',
               font=dict(color='black', size=9))))


    fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="2022 第6回市議会議員選挙",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False, False, False, False, False, False, False]},
                           {"title": "<b>6th City Council Election 2022</b>"}]),
                dict(label="2018 第5回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False, False, False, False, False, False, False]},
                           {"title": "<b>5th City Council Election 2018</b>"}]),
                dict(label="2014 第4回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False, False, False, False, False, False, False]},
                           {"title": "<b>4th City Council Election 2014</b>"}]),
                dict(label="2010 第3回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False, False, False, False, False, False, False]},
                           {"title": "<b>3rd City Council Election 2010</b>"}]),
                dict(label="2006 第2回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False, False, False, False, False, False, False]},
                           {"title": "<b>2nd City Council Election 2006</b>"}]),
                dict(label="2002 第1回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True, False, False, False, False, False, False]},
                           {"title": "<b>1st City Council Election 2002</b>"}]),
                dict(label="2021 第6回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, False, False, False, False, False]},
                           {"title": "<b>6th Mayor Election 2021</b>"}]),
                dict(label="2017 第5回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, True, False, False, False, False]},
                           {"title": "<b>5th Mayor Election 2017</b>"}]),
                dict(label="2013 第4回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, True, False, False, False]},
                           {"title": "<b>4th Mayor Election 2013</b>"}]),
                dict(label="2009 第3回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, True, False, False]},
                           {"title": "<b>3rd City Council Election 2010</b>"}]),
                dict(label="2005 第2回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, False, True, False]},
                           {"title": "<b>2nd Mayor Election 2005</b>"}]),
                dict(label="2001 第1回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, False, False, True]},
                           {"title": "<b>1st Mayor Election 2001</b>"}])
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.85,
            xanchor="right",
            y=1.15,
            yanchor="top"
        )
    ])

    fig.update_layout(paper_bgcolor="aliceblue",
    width=1180,
    height=500,
    autosize=False,
    margin=dict(t=0, b=0, l=0, r=0),
    template="plotly_white",
    )

    fig.update_layout(title='<b>Choose a year</b>')

    return fig

def vote_rate_council_mayor_general(df, n):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    if n==1:
        bgcolor = 'aliceblue'
    else:
        bgcolor = 'lightgray'
    
    fig.add_trace(go.Bar(x=df[df['Type']=='市議']['Year'], y=0.01*df[df['Type']=='市議']['Vote_rate']*df[df['Type']=='市議']['Electrates'], name='市議会議員選挙:投票者数'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df[df['Type']=='市議']['Year'], y=df[df['Type']=='市議']['Vote_rate'], name='市議会議員選挙:投票率'), secondary_y=True)
    fig.add_trace(go.Bar(x=df[df['Type']=='市長']['Year'], y=0.01*df[df['Type']=='市長']['Vote_rate']*df[df['Type']=='市長']['Electrates'], name='市長選挙:投票者数'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df[df['Type']=='市長']['Year'], y=df[df['Type']=='市長']['Vote_rate'], name='市長選挙:投票率'), secondary_y=True)

    fig.update_layout(paper_bgcolor=bgcolor,
                      newshape_line=dict(color = 'black'),
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="City Council",
                     method="update",
                     args=[{"visible": [True, True, False, False]},
                           {"title": "<b>Vote Rate and number of City council election</b>"}]),
                dict(label="Mayor",
                     method="update",
                     args=[{"visible": [False, False, True, True]},
                           {"title": "<b>Vote Rate and number of Mayor election</b>"}]),
                dict(label="City Council & Mayor",
                     method="update",
                     args=[{"visible": [True, True, True, True]},
                           {"title": "<b>Vote Rate and number of City council election and Mayor election</b>"}])
                
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1,
            xanchor="right",
            y=1.3,
            yanchor="top"
       )
    ])
    
    fig.update_layout(title_text="<b>Choose a year</b>", xaxis_title='Year')
    fig.update_yaxes(title_text="Vote Rate", secondary_y=True)
    fig.update_yaxes(title_text="Vote Number", secondary_y=False)
    
    fig.update_layout(
    dragmode="select", hovermode='closest', clickmode='select', template='plotly_white')
    
    return fig

def result_general(df, n):
    fig = go.Figure()
    
    if n==1:
        bgcolor = 'aliceblue'
    else:
        bgcolor = 'lightgray'
        
    button_list = []
    
    for i, year in enumerate(df[df['Type']=='市議']['Year'].unique()):
        all_f = [False]*len(df[df['Type']=='市議']['Year'].unique())
        
        labels_sex=['Elected', 'Not Elected']
        values_sex=[df[(df['Type']=='市議')&(df['Year']==year)]['Result'].value_counts()[1], df[(df['Type']=='市議')&(df['Year']==year)]['Result'].value_counts()[0]]

        all_f[i] = True
        fig.add_trace(go.Pie(labels=labels_sex, values=values_sex, name="{}".format(year)))
        button = dict(label="{}".format(year),
                     method="update",
                     args=[{"visible": all_f},
                           {"title": "<b>Distribution of Result across candidates {}</b>".format(year)}])
        button_list.append(button)

    fig.update_layout(paper_bgcolor=bgcolor,
                      newshape_line=dict(color = 'black'),
    updatemenus=[
        dict(active=0,
            buttons=list(button_list), 
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0,
            xanchor="left",
            y=1,
            yanchor="top")
          ])
    
    fig.update_layout(title_text="<b>Choose a year</b>", template='plotly_white')
    
    return fig     

def sex_general(df, n):
    fig = go.Figure()
    
    if n==1:
        bgcolor = 'aliceblue'
    else:
        bgcolor = 'lightgray'
        
    button_list = []
    
    for i, year in enumerate(df[df['Type']=='市議']['Year'].unique()):
        all_f = [False]*len(df[df['Type']=='市議']['Year'].unique())
        
        labels_sex=['Male', 'Female']
        values_sex=[df[(df['Type']=='市議')&(df['Year']==year)]['Sex'].value_counts()['Male'], df[(df['Type']=='市議')&(df['Year']==year)]['Sex'].value_counts()['Female']]

        all_f[i] = True
        fig.add_trace(go.Pie(labels=labels_sex, values=values_sex, name="{}".format(year)))
        button = dict(label="{}".format(year),
                     method="update",
                     args=[{"visible": all_f},
                           {"title": "<b>Distribution of Sex across candidates {}</b>".format(year)}])
        button_list.append(button)
        
    fig.update_layout(paper_bgcolor=bgcolor,
                      newshape_line=dict(color = 'black'),
    updatemenus=[
        dict(active=0,
            buttons=list(button_list), 
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0,
            xanchor="left",
            y=1,
            yanchor="top")
          ])
    
    fig.update_layout(title_text="<b>Choose a year</b>", template='plotly_white')
    
    return fig 

def party_across_year_general(df, n):
    fig = go.Figure()
    if n==1:
        bgcolor = 'aliceblue'
    else:
        bgcolor = 'lightgray'
        
    button_list = []
    for i, year in enumerate(df[df['Type']=='市議']['Year'].unique()):
        all_f = [False]*len(df[df['Type']=='市議']['Year'].unique())
        fig.add_trace(go.Histogram(name='{}'.format(year), 
        x=df[(df['Year']==year)&(df['Type']=='市議')]['Party']))

        all_f[i] = True

        button = dict(label="{}".format(year),
                     method="update",
                     args=[{"visible": all_f},
                           {"title": "<b>市議会議員立候補者の所属政党 {}</b>".format(year)}])
        button_list.append(button)
        
    fig.update_layout(paper_bgcolor=bgcolor,
                      newshape_line=dict(color = 'mediumblue'),
    updatemenus=[
        dict(
            active=0,
            buttons=list(button_list),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1,
            xanchor="right",
            y=1.35,
            yanchor="top")])

    fig.update_layout(title_text="<b>Choose a year</b>", template='plotly_white')
    
    return fig

def age_general(df, n):
    fig = go.Figure()
    if n==1:
        bgcolor = 'aliceblue'
    else:
        bgcolor = 'lightgray'
        
    button_list = []
    for i, year in enumerate(df[df['Type']=='市議']['Year'].unique()):
        all_f = [False]*len(df[df['Type']=='市議']['Year'].unique())
        all_f[i] = True
        
        fig.add_trace(go.Box(x=df[(df['Type']=='市議')&(df['Year']==year)]['Sex'], 
                             y=df[(df['Type']=='市議')&(df['Year']==year)]['Age'], name='{}'.format(year)))

        button = dict(label="{}".format(year),
                     method="update",
                     args=[{"visible": all_f},
                           {"title": "<b>Distribution of Age across candidates {}</b>".format(year)}])
        button_list.append(button)

    fig.update_layout(paper_bgcolor=bgcolor,
                      newshape_line=dict(color = 'mediumblue'),
    updatemenus=[
        dict(
            active=0,
            buttons=list(button_list),
                direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1,
            xanchor="right",
            y=1.3,
            yanchor="top")
            ])

    fig.update_layout(title_text="<b>Choose a year</b>", template = 'plotly_white')

    return fig

def parcat_general6(df):
    
    fig = go.Figure()
    buttons_tf = []
    count = 0
    
    yunique = df[df['Type']=='市議']['Year'].unique()

    for year in yunique:
        
        allf = [False]*len(yunique)
        df_y = df[(df['Type']=='市議')&(df['Year']==year)]
        
        counts_ln=[]
        for x in ['Age', 'Vote', 'Vote_p']:
            counts=[False]*5
            ag_cut = pd.cut(df_y[x], 5, labels=False)
            df_y[x+'_new']=ag_cut
            for k in dict(ag_cut.value_counts()).keys():
                if dict(ag_cut.value_counts())[k] > 0:
                    counts[k]=True
            counts_ln.append(counts)
                
        df_y['Age_new']=df_y['Age_new'].astype(np.int64)
        df_y['Vote_new']=df_y['Vote_new'].astype(np.int64)
        df_y['Vote_p_new']=df_y['Vote_p_new'].astype(np.int64)
        df_y['Result_p']=df_y['Result_p'].astype(np.int64)
        df_y['Result']=df_y['Result'].astype(np.int64) 
        
        allf[count] = True
        #allf = [True]*len(df[df['Type']=='市議']['Year'].unique())
        buttons_tf.append(allf)
        count += 1
        
        age_min = df_y['Age'].min()
        age_max = df_y['Age'].max()
        da = math.floor((age_max-age_min)/5)
        
        votedrate_min = df_y['Vote'].min()
        votedrate_max = df_y['Vote'].max()
        dvr = math.floor((votedrate_max-votedrate_min)/5)
        
        votedratef_min = df_y['Vote_p'].min()
        votedratef_max = df_y['Vote_p'].max()
        dvrf = math.floor((votedratef_max-votedratef_min)/5)

        age_dim = go.parcats.Dimension(values=df_y['Age_new'], label='AGE', categoryorder='array', 
        categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[0])), 
        ticktext=list(compress(['{}-{}'.format(age_min, age_min+da), '{}-{}'.format(age_min+da, age_min+2*da), 
        '{}-{}'.format(age_min+2*da, age_min+3*da), '{}-{}'.format(age_min+3*da, age_min+4*da), 
        '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])))

        sex_dim = go.parcats.Dimension(values=df_y['Sex'], label="SEX")

        party_dim = go.parcats.Dimension(values=df_y['Party'], label="PARTY")

        votedrate_dim = go.parcats.Dimension(
        values=df_y['Vote_new'], label="VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
        ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, 
                                                                                   votedrate_min+2*dvr), 
        '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, 
                                                                                 votedrate_min+4*dvr), 
        '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[1])))

        votedratef_dim = go.parcats.Dimension(
        values=df_y['Vote_p_new'], label="PREVIOUS VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[2])),
        ticktext=list(compress(['{}-{}'.format(votedratef_min, votedratef_min+dvrf), '{}-{}'.format(votedratef_min+dvrf, 
                                                                                      votedratef_min+2*dvrf), 
        '{}-{}'.format(votedratef_min+2*dvrf, votedratef_min+3*dvrf), '{}-{}'.format(votedratef_min+3*dvrf, 
                                                                                     votedratef_min+4*dvrf), 
        '{}-{}'.format(votedratef_min+4*dvrf, votedratef_min+5*dvrf)], counts_ln[2])))

        if 0 in df_y['Result_p'].unique() and 1 in df_y['Result_p'].unique():

            electedf_dim = go.parcats.Dimension(values=df_y['Result_p'], label='PREVIOUS RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'])
        if 0 not in df_y['Result_p'].unique():
            
            electedf_dim = go.parcats.Dimension(values=df_y['Result_p'], label='PREVIOUS RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'])
        if 1 not in df_y['Result_p'].unique():
            
            electedf_dim = go.parcats.Dimension(values=df_y['Result_p'], label='PREVIOUS RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'])

        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'])
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'])
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'])

        full_ats = [age_dim, sex_dim, party_dim, votedrate_dim, votedratef_dim, electedf_dim, elected_dim]

        color = df_y['Result']
        colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

        fig.add_trace(go.Parcats(dimensions=full_ats,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': 'Times'},
                  tickfont={'size': 13, 'family': 'Times'},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'}))
    
    dict_list = []
    
    for i in range(len(yunique)):
        dict_list.append(dict(
        label="{}".format(yunique[i]),
        method="update",
        args=[{"visible": buttons_tf[i]},
        {"title": "<b>Relation between multiple variables and whether they were elected {}</b>".format(df[df['Type']=='市議']['Year'].unique()[i])}]))
    
    fig.update_layout(paper_bgcolor="lightgray",
        updatemenus=[
            dict(
                active=0,
                buttons=list(dict_list),
    direction="down",
    pad={"r": 10, "t": 10},
    showactive=True,
    x=0,
    xanchor="left",
    y=1.35,
    yanchor="top")
        ])
    
    fig.update_layout(
    width=1200,
    height=600,
    autosize=True,
    margin=dict(t=50, b=50, l=50, r=50),
    template="plotly_white",
    )
    
    fig.show()
    return fig

def parcat_general5(df):
    
    fig = go.Figure()
    buttons_tf = []
    count = 0
    
    yunique = df[df['Type']=='市議']['Year'].unique()

    for year in yunique:
        
        allf = [False]*len(yunique)
        df_y = df[(df['Type']=='市議')&(df['Year']==year)]
        
        counts_ln=[]
        for x in ['Age', 'Vote', 'Vote_p']:
            counts=[False]*5
            ag_cut = pd.cut(df_y[x], 5, labels=False)
            df_y[x+'_new']=ag_cut
            for k in dict(ag_cut.value_counts()).keys():
                if dict(ag_cut.value_counts())[k] > 0:
                    counts[k]=True
            counts_ln.append(counts)
                
        df_y['Age_new']=df_y['Age_new'].astype(np.int64)
        df_y['Vote_new']=df_y['Vote_new'].astype(np.int64)
        df_y['Vote_p_new']=df_y['Vote_p_new'].astype(np.int64)
        df_y['Result_p']=df_y['Result_p'].astype(np.int64)
        df_y['Result']=df_y['Result'].astype(np.int64) 
        
        allf[count] = True
        #allf = [True]*len(df[df['Type']=='市議']['Year'].unique())
        buttons_tf.append(allf)
        count += 1
        
        age_min = df_y['Age'].min()
        age_max = df_y['Age'].max()
        da = math.floor((age_max-age_min)/5)
        
        votedrate_min = df_y['Vote'].min()
        votedrate_max = df_y['Vote'].max()
        dvr = math.floor((votedrate_max-votedrate_min)/5)
        
        votedratef_min = df_y['Vote_p'].min()
        votedratef_max = df_y['Vote_p'].max()
        dvrf = math.floor((votedratef_max-votedratef_min)/5)

        age_dim = go.parcats.Dimension(values=df_y['Age_new'], label='AGE', categoryorder='array', 
        categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[0])), 
        ticktext=list(compress(['{}-{}'.format(age_min, age_min+da), '{}-{}'.format(age_min+da, age_min+2*da), 
        '{}-{}'.format(age_min+2*da, age_min+3*da), '{}-{}'.format(age_min+3*da, age_min+4*da), 
        '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])))

        sex_dim = go.parcats.Dimension(values=df_y['Sex'], label="SEX")

        party_dim = go.parcats.Dimension(values=df_y['Party'], label="PARTY")

        votedrate_dim = go.parcats.Dimension(
        values=df_y['Vote_new'], label="VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
        ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, 
                                                                                   votedrate_min+2*dvr), 
        '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, 
                                                                                 votedrate_min+4*dvr), 
        '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[1])))

        votedratef_dim = go.parcats.Dimension(
        values=df_y['Vote_p_new'], label="PREVIOUS VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[2])),
        ticktext=list(compress(['{}-{}'.format(votedratef_min, votedratef_min+dvrf), '{}-{}'.format(votedratef_min+dvrf, 
                                                                                      votedratef_min+2*dvrf), 
        '{}-{}'.format(votedratef_min+2*dvrf, votedratef_min+3*dvrf), '{}-{}'.format(votedratef_min+3*dvrf, 
                                                                                     votedratef_min+4*dvrf), 
        '{}-{}'.format(votedratef_min+4*dvrf, votedratef_min+5*dvrf)], counts_ln[2])))

        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'])
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'])
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'])

        full_ats = [age_dim, sex_dim, party_dim, votedrate_dim, votedratef_dim, elected_dim]

        color = df_y['Result']
        colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

        fig.add_trace(go.Parcats(dimensions=full_ats,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': 'Times'},
                  tickfont={'size': 13, 'family': 'Times'},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'}))
    
    dict_list = []
    
    for i in range(len(yunique)):
        dict_list.append(dict(
        label="{}".format(yunique[i]),
        method="update",
        args=[{"visible": buttons_tf[i]},
        {"title": "<b>Relation between multiple variables and whether they were elected {}</b>".format(df[df['Type']=='市議']['Year'].unique()[i])}]))
    
    fig.update_layout(paper_bgcolor="lightgray",
        updatemenus=[
            dict(
                active=0,
                buttons=list(dict_list),
    direction="down",
    pad={"r": 10, "t": 10},
    showactive=True,
    x=0,
    xanchor="left",
    y=1.35,
    yanchor="top")
        ])
    
    fig.update_layout(
    width=1200,
    height=600,
    autosize=True,
    margin=dict(t=50, b=50, l=50, r=50),
    template="plotly_white",
    )
    
    fig.show()
    
    return fig

def parcat_general4(df):
    
    fig = go.Figure()
    buttons_tf = []
    count = 0
    
    yunique = df[df['Type']=='市議']['Year'].unique()

    for year in yunique:
        
        allf = [False]*len(yunique)
        df_y = df[(df['Type']=='市議')&(df['Year']==year)]
        
        counts_ln=[]
        for x in ['Age', 'Vote', 'Vote_p']:
            counts=[False]*5
            ag_cut = pd.cut(df_y[x], 5, labels=False)
            df_y[x+'_new']=ag_cut
            for k in dict(ag_cut.value_counts()).keys():
                if dict(ag_cut.value_counts())[k] > 0:
                    counts[k]=True
            counts_ln.append(counts)
                
        df_y['Age_new']=df_y['Age_new'].astype(np.int64)
        df_y['Vote_new']=df_y['Vote_new'].astype(np.int64)
        df_y['Vote_p_new']=df_y['Vote_p_new'].astype(np.int64)
        df_y['Result_p']=df_y['Result_p'].astype(np.int64)
        df_y['Result']=df_y['Result'].astype(np.int64) 
        
        allf[count] = True
        #allf = [True]*len(df[df['Type']=='市議']['Year'].unique())
        buttons_tf.append(allf)
        count += 1
        
        age_min = df_y['Age'].min()
        age_max = df_y['Age'].max()
        da = math.floor((age_max-age_min)/5)
        
        votedrate_min = df_y['Vote'].min()
        votedrate_max = df_y['Vote'].max()
        dvr = math.floor((votedrate_max-votedrate_min)/5)

        age_dim = go.parcats.Dimension(values=df_y['Age_new'], label='AGE', categoryorder='array', 
        categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[0])), 
        ticktext=list(compress(['{}-{}'.format(age_min, age_min+da), '{}-{}'.format(age_min+da, age_min+2*da), 
        '{}-{}'.format(age_min+2*da, age_min+3*da), '{}-{}'.format(age_min+3*da, age_min+4*da), 
        '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])))

        sex_dim = go.parcats.Dimension(values=df_y['Sex'], label="SEX")

        party_dim = go.parcats.Dimension(values=df_y['Party'], label="PARTY")

        votedrate_dim = go.parcats.Dimension(
        values=df_y['Vote_new'], label="VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
        ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, 
                                                                                   votedrate_min+2*dvr), 
        '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, 
                                                                                 votedrate_min+4*dvr), 
        '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[1])))

        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'])
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'])
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'])

        full_ats = [age_dim, sex_dim, party_dim, votedrate_dim, elected_dim]

        color = df_y['Result']
        colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

        fig.add_trace(go.Parcats(dimensions=full_ats,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': 'Times'},
                  tickfont={'size': 13, 'family': 'Times'},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'}))
    
    dict_list = []
    
    for i in range(len(yunique)):
        dict_list.append(dict(
        label="{}".format(yunique[i]),
        method="update",
        args=[{"visible": buttons_tf[i]},
        {"title": "<b>Relation between multiple variables and whether they were elected {}</b>".format(df[df['Type']=='市議']['Year'].unique()[i])}]))
    
    fig.update_layout(paper_bgcolor="lightgray",
        updatemenus=[
            dict(
                active=0,
                buttons=list(dict_list),
    direction="down",
    pad={"r": 10, "t": 10},
    showactive=True,
    x=0,
    xanchor="left",
    y=1.35,
    yanchor="top")
        ])
    
    fig.update_layout(
    width=1200,
    height=600,
    autosize=True,
    margin=dict(t=50, b=50, l=50, r=50),
    template="plotly_white",
    )
    
    fig.show()
    
    return fig

def parcat_general3(df):
    
    fig = go.Figure()
    buttons_tf = []
    count = 0
    
    yunique = df[df['Type']=='市議']['Year'].unique()

    for year in yunique:
        
        allf = [False]*len(yunique)
        df_y = df[(df['Type']=='市議')&(df['Year']==year)]
        
        counts_ln=[]
        for x in ['Age', 'Vote', 'Vote_p']:
            counts=[False]*5
            ag_cut = pd.cut(df_y[x], 5, labels=False)
            df_y[x+'_new']=ag_cut
            for k in dict(ag_cut.value_counts()).keys():
                if dict(ag_cut.value_counts())[k] > 0:
                    counts[k]=True
            counts_ln.append(counts)
                
        df_y['Age_new']=df_y['Age_new'].astype(np.int64)
        df_y['Vote_new']=df_y['Vote_new'].astype(np.int64)
        df_y['Vote_p_new']=df_y['Vote_p_new'].astype(np.int64)
        df_y['Result_p']=df_y['Result_p'].astype(np.int64)
        df_y['Result']=df_y['Result'].astype(np.int64) 
        
        allf[count] = True
        #allf = [True]*len(df[df['Type']=='市議']['Year'].unique())
        buttons_tf.append(allf)
        count += 1
        
        age_min = df_y['Age'].min()
        age_max = df_y['Age'].max()
        da = math.floor((age_max-age_min)/5)

        age_dim = go.parcats.Dimension(values=df_y['Age_new'], label='AGE', categoryorder='array', 
        categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[0])), 
        ticktext=list(compress(['{}-{}'.format(age_min, age_min+da), '{}-{}'.format(age_min+da, age_min+2*da), 
        '{}-{}'.format(age_min+2*da, age_min+3*da), '{}-{}'.format(age_min+3*da, age_min+4*da), 
        '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])))

        sex_dim = go.parcats.Dimension(values=df_y['Sex'], label="SEX")

        party_dim = go.parcats.Dimension(values=df_y['Party'], label="PARTY")
        
        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'])
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'])
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'])    
        

        full_ats = [age_dim, sex_dim, party_dim, elected_dim]

        color = df_y['Result']
        colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

        fig.add_trace(go.Parcats(dimensions=full_ats,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': 'Times'},
                  tickfont={'size': 13, 'family': 'Times'},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'}))
        
    dict_list = []
    for i in range(len(yunique)):
    
        label="{}".format(yunique[i])
        title="<b>Relation between multiple variables and whether they were elected {}</b>".format(yunique[i])

        dict_list.append(dict(
        label=label,
        method="update",
        args=[{"visible": buttons_tf[i]},
        {"title": title}]))
    
    fig.update_layout(paper_bgcolor="lightgray",
        updatemenus=[
            dict(
                active=0,
                buttons=list(dict_list),
    direction="down",
    pad={"r": 10, "t": 10},
    showactive=True,
    x=0,
    xanchor="left",
    y=1.35,
    yanchor="top")
    ])
    
    fig.update_layout(
    width=1200,
    height=600,
    autosize=True,
    margin=dict(t=50, b=50, l=50, r=50),
    template='plotly_white'
    )
    
    fig.show()
    
    return fig


# In[2]:


layout = dbc.Container([html.Br(),
                html.Div(html.H1('POLITICS', className='display-1',
                        style={'textAlign':'left', 'color':'midnightblue', 'font-size':30})
                        ),
                html.Div('西東京市の政治についての分析を見る。ほかの自治体の政治を分析する。'
                         , className="fw-light",
                style=
                {'font-family':'游明朝', 'textAlign':'left', 'color':'royalblue', 'font-size':20}),
                html.Br(),
                html.Br(),
                html.Div(
            [
               dbc.Button(
                    "ABOUT",
                    id="about-offcanvas-scrollable",
                   n_clicks=0,
               ),
               dbc.Offcanvas(
                    [html.Hr(), html.P(
                    "A resource for knowing, learning about and\ngetting excited about city council election,\ndesigned mainly for Nishi Tokyo City, Tokyo,\nbut can be applied to any other city."
                    ),
                     html.P("-Figures on elections held in Nishi Tokyo City"), 
                     html.P("-Quick review on Nishi Tokyo City Council"), 
                     html.P("-Uploading your city's data and getting figures out"), html.Br(),
                    dcc.Markdown('''
                    **Contact : westt-sskry(at)gmail.com**
                    ''')],
                    id="offcanvas-scrollable",
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
                  dbc.Button('?', outline=True, color='info', style={'textAlign': 'center', 'font-size': 15}, n_clicks=0, id='doc_button1')
                 ]),
        html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('GRAPH DESCRIPTION'),
            dbc.CardBody([
            html.P( 
            dcc.Markdown('''
            *PARTY*: Counts for each Party
            
            *SEX*: Distribution of Sex (Male or Female) across the candidates
            
            *AGE*: Distribution of Age across the candidates
            
            *VOTE RATE*: Vote Rate of each election
            
            *RESULT*: Distribution of Result(Elected or not) across the candidates'
            ''')), html.P([html.B('Source'), dcc.Markdown('''
            https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html
            ''')])])],
            color='info', outline = True),
            id='doc1',
            is_open=False,
        )),
        html.Hr(),
        html.Br(),
        html.Br(),
        html.Div(dbc.Tabs([
        dbc.Tab(label='PARTY', children=[
            dcc.Graph(
                figure=party_across_year_general(df, 1))
        ]),
        dbc.Tab(label='SEX', children=[
            dcc.Graph(figure=sex_general(df, 1)
            )
        ]),
        dbc.Tab(label='AGE', children=[
            dcc.Graph(
                figure=age_general(df, 1)
            )
        ]),
        dbc.Tab(label='VOTE RATE', children=[
            dcc.Graph(
                figure=vote_rate_council_mayor_general(df_vote_rate, 1)
            )
        ]),
        dbc.Tab(label='RESULT', children=[
            dcc.Graph(
                figure=result_general(df, 1)
            )
        ])
    ])
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('Candidates Name, Pledges and other info', 
                               style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
             dbc.Button('?', outline=True, color='info', style={'textAlign': 'center', 'font-size': 15}, n_clicks=0, id='doc_button2')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('TABLE DESCRIPTION'),
            dbc.CardBody([
            html.P(dcc.Markdown('''
            *Pledges, Career*: Extracted from Election Gazetta of each candidate. 
            
            (*i.e* these could be reflecting editor's bias) 
            
            Candidates whose columns are highlighted in pink were elected and in blue not."
            ''')), html.P([html.B('Source'), dcc.Markdown('''
            https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html
            ''')])])],
            color='dark', outline = True),
            id='doc2',
            is_open=False,
        )),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.Div(dbc.Spinner(dcc.Graph(figure = candidate_info(df_table)), color='dark')),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('Relationship between multiple attributes and the Election Result', 
                      style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}), 
             dbc.Button('?', outline=True, color='info', style={'textAlign': 'center', 'font-size': 15}, n_clicks=0, id='doc_button3')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('GRAPH DESCRIPTION'),
            dbc.CardBody([
            html.P( 
            dcc.Markdown('''
            Each rectangle corresponds to a discrete value taken on by that variable. 
            The relative heights of the rectangles reflect the relative frequency of 
            occurrence of the corresponding value.
            Combinations of category rectangles across dimensions are connected by ribbons, 
            where the height of the ribbon corresponds to the relative frequency of 
            occurrence of the combination of categories in the data set.
            
            Ribbons highlighted in green are those of candidates elected.
            
            *PREVIOUS VOTE/ VOTE(%)/ RESULT*: 
            If a candidate hasn't run for the previous election, 0/ Not Elected was assigned for them.
            ''')), html.P([html.B('Source'), dcc.Markdown('''
            https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html
            ''')])])],
            color='secondary', outline = True),
            id='doc3',
            is_open=False,
        )),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.Div(['Choose a year: ', dcc.Dropdown([2022, 2018, 2014, 2010, 2006, 2002], 2022, id='input-year', clearable=False)
             ]),
    
    html.Div([html.Div(['Choose Attributes: ', 
    dcc.Checklist(['AGE', 'SEX', 'PARTY', 'VOTE', 'VOTE(%)', 'PREVIOUS VOTE', 'PREVIOUS VOTE(%)', 'PREVIOUS RESULT'], id='attributes', inline=True,
                  style = {'display': 'flex'}
                 )])]),
    html.Div(dbc.Button(id='submit-button-state1', n_clicks=0, children='Select Values', color='info')),
    html.Br(),
    html.Div(id='selection_completed'),
    html.Br(),
    html.Div(dcc.Graph(id='parcat')),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('City Council Review', style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
             dbc.Button('?', outline=True, color='info', 
                        style={'textAlign': 'center', 'font-size': 15, 'className':'mb-3'}, n_clicks=0, id='doc_button5')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('GRAPH DESCRIPTION'),
            dbc.CardBody([
            html.P( 
            dcc.Markdown('''
            Each circle corresponds to a noun observed in the minutes of Nishi Tokyo of the year, 
            the size of which indicates its adjacency, so the bigger the more important it is, and 
            the color of which indicates grouping.
            
            Lines(edges) are drawn between words which appear together.
    
            
            **Algorithm** 
            
            *1. Text Processing*
            
            -For each line of a minutes, nouns except numbers, human names and suffixes were extracted.
            -Then, tf-idf (term-frequency times inverse document-frequency) transformation was performed
             on them, where frequent but less meaningful terms were scored lower, and less frequent but 
             meaningful ones were scored higher. 
             For more info: 
             https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
             
             $$
             tf-idf(noun,\ minutes) = tf(noun,\ minutes)\\times{idf(noun)}
             $$
             
             $$
             tf(noun, minutes) = The\ number\ of\ times\ a\ noun\ occurs\ in\ a\ minutes
             $$
             
             $$
             idf(noun) = 
             \\ln{\\frac{1 + Number\ of\ lines\ in\ a\ minute}{1 + Number\ of\ lines\ that\ contain\ the\ noun}} + 1
             $$
             
             -Top 100 nouns regarding the tf-idf score were extracted.  
             
             *2. Coocurrance network graph calculation*
             
             -On the 100 nouns, algorithmns for NetworkX was performed.
             https://networkx.org/documentation/stable/reference/algorithms/index.html
            
            ''', mathjax=True)), html.P([html.B('Source'), html.Div('https://www.city.nishitokyo.tokyo.dbsr.jp/index.php/')])])],
            color='light', outline = True),
            id='doc5',
            is_open=False,
        )),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.Div(['Choose a year: ', dcc.Dropdown([y for y in reversed(range(2001, 2023))], 
    2022, id='input-year-network', clearable=False)
             ]),
    html.Br(),
    html.Div(dbc.Spinner(dcc.Graph(id = 'network'), color='dark')),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('Make graphs of your city!', style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
             dbc.Button('?', outline=True, color='info', 
                        style={'textAlign': 'center', 'font-size': 15, 'className':'mb-3'}, n_clicks=0, id='doc_button4')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('DESCRIPTION'),
            dbc.CardBody([html.P(dcc.Markdown('''
            By uploading csv files, you can obtain figures. File format restriction is strict. 
            Please see below for the info.
            '''))])],
            color='primary', outline = True),
            id='doc4',
            is_open=False,
        )),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.H3('Basic Statistical Figures', style={'textAlign': 'left', 'color': '#503D36', 'font-size': 20}),
    
    html.Div([
    dcc.Upload(
        id='upload-data',
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
        # Allow multiple files to be uploaded
        multiple=False
    )]),
    
    html.H3('Your Graphs:', style={'font-size':20}),
    html.Br(),
    html.Div(id='output-data-upload'),
    html.Br(),
    html.H3('Relationship between multiple attributes and the Election Result', 
            style={'textAlign': 'left', 'color': '#503D36', 'font-size': 20}),
    
    html.Div([
    dcc.Upload(
        id='upload-data2',
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
        # Allow multiple files to be uploaded
        multiple=False
    )]),
    
    html.H3('Your Graphs:', style={'font-size':20}),
    html.Br(),
    html.Div([
        dbc.Tabs([
            dbc.Tab(tab_id='SET 1', label='SET 1', children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")])
        ]),
        dbc.Tab(tab_id='SET 2', label='SET 2', children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")
            , dbc.Badge('VOTE(%)', text_color="dark", color="light")])
        ]),
        dbc.Tab(tab_id='SET 3', label='SET 3', children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")
            , dbc.Badge('VOTE(%)', text_color="dark", color="light"),
            dbc.Badge('PREVIOUS VOTE(%)', text_color="dark", color="light")])
        ]),
        dbc.Tab(tab_id='SET 4', label='SET 4', children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")
            , dbc.Badge('VOTE(%)', text_color="dark", color="light"),
            dbc.Badge('PREVIOUS VOTE(%)', text_color="dark", color="light"),
            dbc.Badge('PREVIOUS RESULT', text_color="dark", color="light")])
        ])
    ], id='upload2_tabs')
    ]), 
    html.Br(), dbc.Button(id='submit-button-state2', n_clicks=0, children='Change Sets', color='info'),
    html.Div(id='selection_completed2'),
    html.Div(id = 'upload2_set')
    ,
    html.Br(),
    html.Br(),
    html.H3('File Format'),
    html.Br(),
    html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [html.P([html.B("File Type"),html.Div("-CSV")]), html.P([html.B("Encoding"), html.Div("-Shift JIS")]), 
                 html.P([html.B("Columns"),dcc.Markdown('''
                *-Age* (Age of a candidate)
                
                *-Sex* (Sex of a candidate, Male or Female)
                
                *-Year* (Year when the candidate ran for the election)
                
                *-Party* (A party a candidate belongs to)
                
                *-Vote_rate* (Vote rate of the election)
                
                *-Electrates* (Number of electrates in the election)
                
                *-Type* (Election type, 市議or市長)
                
                *-Result* (Whether the candidate were elected, 1 for elected, 0 for not)
                
                *-Candidate:optional* (Name of a candidate)
                 ''')]),
                html.P([html.B("Note"), html.Div("-Columns which have nulls (NaNs, N/As) are deleted automatically")])]
                , title="Basic Statistical Figures"
            ),
            dbc.AccordionItem([html.P([html.B("File Type"), html.Div("-CSV")]), html.P([html.B("Encoding"),html.Div("-Shift JIS")]), 
                               html.P([html.B("Columns"), dcc.Markdown('''
                *-Age* (Age of a candidate)
                
                *-Sex* (Sex of a candidate, Male or Female)
                
                *-Year* (Year when the candidate ran for the election)
                
                *-Party* (A party a candidate belongs to)
                
                *-Type* (Election type, 市議or市長)
                
                *-Vote* (Votes received in the election (%))
                
                *-Vote_num* (Votes received in the election)
                
                *-Result* (Whether the candidate were elected, 1 for elected, 0 for not)
                
                *-Vote_p* (Votes received in the previous election (%))
                
                *-Vote_num_p* (Votes received in the previous election)
                
                *-Result_p* (Whether the candidate were elected in the previous election, 1 for elected, 0 for not)
                
                *-Candidate:optional* (Name of a candidate)
                ''')]), 
                html.P([html.B("Note"), html.Div("-Columns which have nulls (NaNs, N/As) are deleted automatically")])]
                , title="Relationship between multiple attributes and the Election Result")
            ,
                 ],
                 flush=True,
                 start_collapsed=True,
             ),
        ),
    html.Br()
])


# In[ ]:


def get_df(year):
    df = df_filtered_list[year-2001]
    return df

@callback(Output('network', 'figure'),
         Input('input-year-network', 'value')
         )

def get_network(year):
    
    df = get_df(year)
    npt = nlplot.NLPlot(df, target_col='selectednouns')
    npt.build_graph(min_edge_frequency=5)

    fig_co_network = npt.co_network(
    title='{}'.format(year),
    sizing=100,
    node_size='adjacency_frequency',
    color_palette='hls',
    width=1100,
    height=1000,
    save=False
    )
    return fig_co_network


@callback(
    Output("offcanvas-scrollable", "is_open"),
    Input("about-offcanvas-scrollable", "n_clicks"),
    State("offcanvas-scrollable", "is_open"),
)
def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(
    Output("doc1", "is_open"),
    Input("doc_button1", "n_clicks"),
    State("doc1", "is_open"),
)
def toggle_collapse1(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("doc2", "is_open"),
    Input("doc_button2", "n_clicks"),
    State("doc2", "is_open"),
)
def toggle_collapse2(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("doc3", "is_open"),
    Input("doc_button3", "n_clicks"),
    State("doc3", "is_open"),
)
def toggle_collapse3(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("doc4", "is_open"),
    Input("doc_button4", "n_clicks"),
    State("doc4", "is_open"),
)
def toggle_collapse4(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("doc5", "is_open"),
    Input("doc_button5", "n_clicks"),
    State("doc5", "is_open"),
)
def toggle_collapse5(n, is_open):
    if n:
        return not is_open
    return is_open

def parse_content(content, filename):
    content_type, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df_in = pd.read_csv(
                io.StringIO(decoded.decode('shift-jis')))
            
            df_in.dropna(subset=['Type', 'Year', 'Age', 'Vote', 'Vote_p', 'Sex', 'Party', 'Result', 'Result_p'], inplace=True)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div(dbc.Tabs([
        dbc.Tab(label='Party', children=[
            dcc.Graph(
                figure=party_across_year_general(df_in, 0))
        ]),
        dbc.Tab(label='Sex', children=[
            dcc.Graph(figure=sex_general(df_in, 0)
            )
        ]),
        dbc.Tab(label='Age', children=[
            dcc.Graph(
                figure=age_general(df_in, 0)
            )
        ]),
        dbc.Tab(label='Vote Rate', children=[
            dcc.Graph(
                figure=vote_rate_council_mayor_general(df_in, 0)
            )
        ]),
        dbc.Tab(label='Result', children=[
            dcc.Graph(
                figure=result_general(df_in, 0)
            )
        ])
    ])
    )

@callback(
          Output('output-data-upload', 'children'),
               Input('upload-data', 'contents'),
               State('upload-data', 'filename')
             )

def update_output(content, name):
    if content is not None:
        try:
            children = [parse_content(content, name)]
    
        except Exception as e:
            print(e)
    
            return [html.Div('There was an error processing this file.')]
    
        return children
    
def parcat_dash(entered_year, entered_attributes):
    
    if entered_attributes is None or len(entered_attributes) == 0:
        raise PreventUpdate
            
    else:
        
        if not isinstance(entered_attributes, list):
            entered_attributes = [entered_attributes]
            
            df = df_table_city[df_table_city['Year']==entered_year]
        
            df.dropna(subset=['Type', 'Year', 'Age', 'Vote', 'Vote_p', 'Sex', 'Party', 'Result', 'Result_p', 'Vote_num', 'Vote_num_p'], inplace=True)
                        
            counts_ln = []
            for x in ['Age', 'Vote_num', 'Vote', 'Vote_num_p', 'Vote_p']:
                counts = [False]*5
                ag_cut = pd.cut(df[x], 5, labels=False)
                df[x+'_new']=ag_cut
                count = ag_cut.value_counts()
                for k in dict(count).keys():
                    if count[k] > 0:
                        counts[k] = True
                counts_ln.append(counts)
                
            df['Age_new'] = df['Age_new'].astype(np.int64)
            df['Vote_new'] = df['Vote_new'].astype(np.int64)
            df['Vote_p_new'] = df['Vote_p_new'].astype(np.int64)
            df['Vote_num_new'] = df['Vote_num_new'].astype(np.int64)
            df['Vote_num_p_new'] = df['Vote_num_p_new'].astype(np.int64)
            df['Result_p'] = df['Result_p'].astype(np.int64)
            df['Result'] = df['Result'].astype(np.int64)
        
            ats   = ['AGE', 'SEX', 'PARTY', 'VOTE', 'VOTE(%)', 'PREVIOUS VOTE', 'PREVIOUS VOTE(%)', 'PREVIOUS RESULT']
            tf = [False]*len(ats)
            for i in range(len(ats)):
                if ats[i] in entered_attributes:
                    tf[i] = True
            age_min = df['Age'].min()
            age_max = df['Age'].max()
            da = math.floor((age_max-age_min)/5)

            vote_min = df['Vote_num'].min()
            vote_max = df['Vote_num'].max()
            dv = math.floor((vote_max-vote_min)/5)

            votedrate_min = df['Vote'].min()
            votedrate_max = df['Vote'].max()
            dvr = math.floor((votedrate_max-votedrate_min)/5)

            votef_min = df['Vote_num_p'].min()
            votef_max = df['Vote_num_p'].max()
            dvf = math.floor((votef_max-votef_min)/5)

            votedratef_min = df['Vote_p'].min()
            votedratef_max = df['Vote_p'].max()
            dvrf = math.floor((votedratef_max-votedratef_min)/5)
    
    
            age_dim = go.parcats.Dimension(values=df['Age_new'], label='AGE', categoryorder='array', 
                     categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[0])),
                     ticktext=list(compress(['{}-{}'.format(age_min, age_min+da), '{}-{}'.format(age_min+da, age_min+2*da), 
                     '{}-{}'.format(age_min+2*da, age_min+3*da), '{}-{}'.format(age_min+3*da, age_min+4*da), 
                     '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])))

            sex_dim = go.parcats.Dimension(values=df['Sex'], label="SEX")

            party_dim = go.parcats.Dimension(values=df['Party'], label="PARTY")
 
            vote_dim = go.parcats.Dimension(values=df['Vote_num_new'], label='VOTE', categoryorder='array', 
                      categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
                      ticktext=list(compress(['{}-{}'.format(vote_min, vote_min+dv), '{}-{}'.format(vote_min+dv, vote_min+2*dv), 
                      '{}-{}'.format(vote_min+2*dv, vote_min+3*dv), '{}-{}'.format(vote_min+3*dv, vote_min+4*dv), 
                      '{}-{}'.format(vote_min+4*dv, vote_min+5*dv)], counts_ln[1])))

            votedrate_dim = go.parcats.Dimension(values=df['Vote_new'], label="VOTE(%)", categoryorder='array', 
                           categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[2])),
                           ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, votedrate_min+2*dvr), 
                           '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, votedrate_min+4*dvr), 
                           '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[2])))

            votef_dim = go.parcats.Dimension(values=df['Vote_num_p_new'], label='PREVIOUS VOTE', categoryorder='array', 
                       categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[3])),
                       ticktext=list(compress(['{}-{}'.format(votef_min, votef_min+dvf), '{}-{}'.format(votef_min+dvf, votef_min+2*dvf), 
                       '{}-{}'.format(votef_min+2*dvf, votef_min+3*dvf), '{}-{}'.format(votef_min+3*dvf, votef_min+4*dvf), 
                       '{}-{}'.format(votef_min+4*dvf, votef_min+5*dvf)], counts_ln[3])))

            votedratef_dim = go.parcats.Dimension(values=df['Vote_p_new'], label="PREVIOUS VOTE(%)", categoryorder='array', 
                            categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[4])),
                            ticktext=list(compress(['{}-{}'.format(votedratef_min, votedratef_min+dvrf), '{}-{}'.format(votedratef_min+dvrf, votedratef_min+2*dvrf), 
                            '{}-{}'.format(votedratef_min+2*dvrf, votedratef_min+3*dvrf), '{}-{}'.format(votedratef_min+3*dvrf, votedratef_min+4*dvrf), 
                            '{}-{}'.format(votedratef_min+4*dvrf, votedratef_min+5*dvrf)], counts_ln[4])))

            if 0 in df['Result_p'].unique() and 1 in df['Result_p'].unique():

                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[0, 1], categoryorder = 'array',
                          ticktext=['Not elected', 'Elected'])
                
            if 0 not in df['Result_p'].unique():
                
                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[1], categoryorder = 'array',
                          ticktext=['Elected'])
                
            if 1 not in df['Result_p'].unique():
                
                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[0], categoryorder = 'array',
                          ticktext=['Not Elected'])
    
            if 0 in df['Result'].unique() and 1 in df['Result'].unique():
    
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[0, 1], categoryorder = 'array',
                          ticktext=['Not elected', 'Elected'])
        
            if 0 not in df['Result'].unique():       
                
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[1], categoryorder = 'array',
                          ticktext=['Elected'])
                
            if 1 not in df['Result'].unique():
                
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[0], categoryorder = 'array',
                          ticktext=['Not Elected'])
                
            full_ats = [age_dim, sex_dim, party_dim, vote_dim, votedrate_dim, votef_dim, votedratef_dim, electedf_dim]

            dimensions = []
            for i in range(len(tf)):
                if tf[i]:
                    dimensions.append(full_ats[i])
            dimensions.append(elected_dim)

            color = df['Result']
            colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

            fig = go.Figure(
                  data = [go.Parcats(dimensions=dimensions,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': 'Times'},
                  tickfont={'size': 13, 'family': 'Times'},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'})])
            
            fig.update_layout(paper_bgcolor = 'lavenderblush',
                             title = '<b>{}</b>'.format(entered_year))
            
            fig.show()
    
            return fig
    
        if isinstance(entered_attributes, list):
            
            df = df_table_city[df_table_city['Year']==entered_year]
        
            df.dropna(subset=['Type', 'Year', 'Age', 'Vote', 'Vote_p', 'Sex', 'Party', 'Result', 'Result_p', 'Vote_num', 'Vote_num_p'], inplace=True)

            counts_ln = []
            for x in ['Age', 'Vote_num', 'Vote', 'Vote_num_p', 'Vote_p']:
                counts = [False]*5
                ag_cut = pd.cut(df[x], 5, labels=False)
                df[x+'_new']=ag_cut
                count = ag_cut.value_counts()
                for k in dict(count).keys():
                    if count[k] > 0:
                        counts[k] = True
                counts_ln.append(counts)
    
            df['Age_new'] = df['Age_new'].astype(np.int64)
            df['Vote_new'] = df['Vote_new'].astype(np.int64)
            df['Vote_p_new'] = df['Vote_p_new'].astype(np.int64)
            df['Vote_num_new'] = df['Vote_num_new'].astype(np.int64)
            df['Vote_num_p_new'] = df['Vote_num_p_new'].astype(np.int64)
            df['Result_p'] = df['Result_p'].astype(np.int64)
            df['Result'] = df['Result'].astype(np.int64)
        
            ats   = ['AGE', 'SEX', 'PARTY', 'VOTE', 'VOTE(%)', 'PREVIOUS VOTE', 'PREVIOUS VOTE(%)', 'PREVIOUS RESULT']
            tf = [False]*len(ats)
            for i in range(len(ats)):
                if ats[i] in entered_attributes:
                    tf[i] = True
                    
            age_min = df['Age'].min()
            age_max = df['Age'].max()
            da = math.floor((age_max-age_min)/5)

            vote_min = df['Vote_num'].min()
            vote_max = df['Vote_num'].max()
            dv = math.floor((vote_max-vote_min)/5)

            votedrate_min = df['Vote'].min()
            votedrate_max = df['Vote'].max()
            dvr = math.floor((votedrate_max-votedrate_min)/5)

            votef_min = df['Vote_num_p'].min()
            votef_max = df['Vote_num_p'].max()
            dvf = math.floor((votef_max-votef_min)/5)

            votedratef_min = df['Vote_p'].min()
            votedratef_max = df['Vote_p'].max()
            dvrf = math.floor((votedratef_max-votedratef_min)/5)
    
    
            age_dim = go.parcats.Dimension(values=df['Age_new'], label='AGE', categoryorder='array', 
                     categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[0])),
                     ticktext=list(compress(['{}-{}'.format(age_min, age_min+da), '{}-{}'.format(age_min+da, age_min+2*da), 
                     '{}-{}'.format(age_min+2*da, age_min+3*da), '{}-{}'.format(age_min+3*da, age_min+4*da), 
                     '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])))

            sex_dim = go.parcats.Dimension(values=df['Sex'], label="SEX")

            party_dim = go.parcats.Dimension(values=df['Party'], label="PARTY")
 
            vote_dim = go.parcats.Dimension(values=df['Vote_num_new'], label='VOTE', categoryorder='array', 
                      categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
                      ticktext=list(compress(['{}-{}'.format(vote_min, vote_min+dv), '{}-{}'.format(vote_min+dv, vote_min+2*dv), 
                      '{}-{}'.format(vote_min+2*dv, vote_min+3*dv), '{}-{}'.format(vote_min+3*dv, vote_min+4*dv), 
                      '{}-{}'.format(vote_min+4*dv, vote_min+5*dv)], counts_ln[1])))

            votedrate_dim = go.parcats.Dimension(values=df['Vote_new'], label="VOTE(%)", categoryorder='array', 
                           categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[2])),
                           ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, votedrate_min+2*dvr), 
                           '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, votedrate_min+4*dvr), 
                           '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[2])))

            votef_dim = go.parcats.Dimension(values=df['Vote_num_p_new'], label='PREVIOUS VOTE', categoryorder='array', 
                       categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[3])),
                       ticktext=list(compress(['{}-{}'.format(votef_min, votef_min+dvf), '{}-{}'.format(votef_min+dvf, votef_min+2*dvf), 
                       '{}-{}'.format(votef_min+2*dvf, votef_min+3*dvf), '{}-{}'.format(votef_min+3*dvf, votef_min+4*dvf), 
                       '{}-{}'.format(votef_min+4*dvf, votef_min+5*dvf)], counts_ln[3])))

            votedratef_dim = go.parcats.Dimension(
                            values=df['Vote_p_new'], label="PREVIOUS VOTE(%)", categoryorder='array', 
                            categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[4])),
                            ticktext=list(compress(['{}-{}'.format(votedratef_min, votedratef_min+dvrf), '{}-{}'.format(votedratef_min+dvrf, votedratef_min+2*dvrf), 
                            '{}-{}'.format(votedratef_min+2*dvrf, votedratef_min+3*dvrf), '{}-{}'.format(votedratef_min+3*dvrf, votedratef_min+4*dvrf), 
                            '{}-{}'.format(votedratef_min+4*dvrf, votedratef_min+5*dvrf)], counts_ln[4])))
            
            if 0 in df['Result_p'].unique() and 1 in df['Result_p'].unique():

                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[0, 1], categoryorder = 'array',
                          ticktext=['Not elected', 'Elected'])
                
            if 0 not in df['Result_p'].unique():
                
                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[1], categoryorder = 'array',
                          ticktext=['Elected'])
                
            if 1 not in df['Result_p'].unique():
                
                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[0], categoryorder = 'array',
                          ticktext=['Not Elected'])
    
            if 0 in df['Result'].unique() and 1 in df['Result'].unique():
    
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[0, 1], categoryorder = 'array',
                          ticktext=['Not elected', 'Elected'])
        
            if 0 not in df['Result'].unique():       
                
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[1], categoryorder = 'array',
                          ticktext=['Elected'])
                
            if 1 not in df['Result'].unique():
                
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[0], categoryorder = 'array',
                          ticktext=['Not Elected'])

            full_ats = [age_dim, sex_dim, party_dim, vote_dim, votedrate_dim, votef_dim, votedratef_dim, electedf_dim]

            dimensions = []
            for i in range(len(tf)):
                if tf[i]:
                    dimensions.append(full_ats[i])
            dimensions.append(elected_dim)

            color = df['Result']
            colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

            fig = go.Figure(data = [go.Parcats(dimensions=dimensions,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': 'Times'},
                  tickfont={'size': 13, 'family': 'Times'},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'})])
            
            fig.update_layout(paper_bgcolor = 'lavenderblush',
                width=1200,
                height=600,
                autosize=True,
                margin=dict(t=50, b=80, l=50, r=80),
                template="plotly_white",
                title = '<b>{}</b>'.format(entered_year)
                )
            
            fig.show()   
            
            return fig

            
@callback(Output('parcat', 'figure'),
               State('input-year', 'value'),
               State('attributes', 'value'),
               Input('submit-button-state1', 'n_clicks')
             )
def update_parcat(entered_year, entered_attributes, n_clicks):
    if n_clicks%2 == 1:
        fig = parcat_dash(entered_year, entered_attributes)
        return fig
    
    else:
        raise PreventUpdate
        
@callback(Output('selection_completed', 'children'),
         Input('submit-button-state1', 'n_clicks'))

def completion_alert(n_clicks):
    if n_clicks%2 == 1:
        return [dbc.Alert("Submitted!!! (Press the button again before changing values again)", color="secondary")]
    
    else:
        return [dbc.Alert("Please select values and press submit button", color="info")]


def parse_content2(content2, at, filename2, n):
    content_type, content_string = content2.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename2:
            # Assume that the user uploaded a CSV file
            df_in = pd.read_csv(
                io.StringIO(decoded.decode('shift-jis')))
            
            df_in.dropna(subset=['Type', 'Year', 'Age', 'Vote', 'Vote_p', 'Sex', 'Party', 'Result'], inplace=True)

    except Exception as e:
        print(e)
        return None
    return df_in

@callback(
          Output('upload2_set', 'children'),
               Input('upload-data2', 'contents'),
               State('upload2_tabs', 'active_tab'),
               State('upload-data2', 'filename'),
               Input('submit-button-state2', 'n_clicks')
             )

def update_output2(content2, at, filename2, n):
    if content2 is not None and n%2==1:
        
        if parse_content2(content2, at, filename2, n) is not None:
            if at=='SET 1':
                return [html.Div(
                    dcc.Graph(figure=parcat_general3(parse_content2(content2, at, filename2, n))))]
            
            if at=='SET 2':
                return [html.Div(
                    dcc.Graph(figure=parcat_general4(parse_content2(content2, at, filename2, n))))]
        
            if at=='SET 3':
                return [html.Div(
                    dcc.Graph(figure=parcat_general5(parse_content2(content2, at, filename2, n))))]
            
            if at=='SET 4':
                return [html.Div(
                    dcc.Graph(figure=parcat_general6(parse_content2(content2, at, filename2, n))))]   
                
        else:
            return [html.Div('There was an error processing this file.')]
    else:
        raise PreventUpdate
        
@callback(Output('selection_completed2', 'children'),
          Input('upload-data2', 'contents'),
         Input('submit-button-state2', 'n_clicks'))

def completion_alert(content2, n_clicks):
    if (n_clicks%2 == 1)&(content2 is not None):
        return [dbc.Alert("Submitted!!! (Press the button again before changing sets)", color="secondary")]
    
    if (n_clicks%2 == 0)&(content2 is not None):
        return [dbc.Alert("Please select a set and press the button", color="info")]
    
    else:
        return [html.Section()]


# In[ ]:




