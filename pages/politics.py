#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import ast
from dash import html
from dash import dcc
import nlplot
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import base64
import io
from dash import callback, State
from dash.dependencies import Input, Output
from plotly.colors import n_colors
from itertools import compress
import math
import dash_bootstrap_components as dbc
import json
import plotly

font_fam_sp = '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'

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
    colors = n_colors('rgb(169, 181, 255)', 'rgb(255, 169, 236)', 2, colortype='rgb')
    for year in df[df['Type']=='市議']['Year'].unique():
        df_y = df[(df['Year']==year)&(df['Type']=='市議')]

        columnorder = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        columnwidth = [1.5, 1.1, 1, 1, 3.2, 3.2, 3, 3.2, 3, 1.2, 1.2, 1.8, 1.8]
        
        fig.add_trace(go.Table(columnorder=columnorder, columnwidth=columnwidth, name='Candidates of {} city council election'.format(year),
        header=dict(values=[['<b>NAME</b>'], ['<b>PARTY</b>'], ['<b>AGE</b>'], ['<b>SEX</b>'], ['<b>CAREER</b>'], 
                ['<b>EDUCATIONAL</b><br><b>PLEDGE</b>'], ['<b>WELFARE</b><br><b>PLEDGE</b>'], 
                ['<b>CITYPLANNING</b><br><b>PLEDGE</b>'], ['<b>OTHER</b><br><b>PLEDGE</b>'], ['<b>VOTES<br></b>'], 
                ['<b>VOTES<br></b>(%)'], ['<b>PREVIOUS<br>VOTES<br></b>'], ['<b>PREVIOUS<br>VOTES<br></b>(%)']],
                fill_color="#d9e3f1",
                align='left',
                font_size=10,
                font=dict(color='navy')),
        cells=dict(values=[df_y.Candidate, df_y.Party, df_y.Age, df_y.Sex, df_y.Career, df_y.edu, df_y.wel, df_y.city, df_y.other, 
                           df_y.Vote_num, df_y.Vote, df_y.Vote_num_p, df_y.Vote_p],
               fill_color=[np.array(colors)[list(map(int, df_y.Result))]]*13,
               align='left',
               font=dict(color='black', size=12))))

    for year in df[df['Type']=='市長']['Year'].unique():
        df_y_mayor = df[(df['Year']==year)&(df['Type']=='市長')]

        columnorder = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        columnwidth = [1.5, 1.1, 1, 1, 3.2, 3.2, 3, 3.2, 3, 1.2, 1.2, 1.8, 1.8]
        
        fig.add_trace(go.Table(columnorder=columnorder, columnwidth=columnwidth, name='Candidates of {} mayor election'.format(year),
        header=dict(values=[['<b>NAME</b>'], ['<b>PARTY</b>'], ['<b>AGE</b>'], ['<b>SEX</b>'], ['<b>CAREER</b>'], 
                ['<b>EDUCATIONAL</b><br><b>PLEDGE</b>'], ['<b>WELFARE</b><br><b>PLEDGE</b>'], 
                ['<b>CITYPLANNING</b><br><b>PLEDGE</b>'], ['<b>OTHER</b><br><b>PLEDGE</b>'], ['<b>VOTES<br></b>'], 
                ['<b>VOTES<br></b>(%)'], ['<b>PREVIOUS<br>VOTES</b>'], ['<b>PREVIOUS<br>VOTES</b><br>(%)']],
                fill_color="#d9e3f1",
                align='left',
                font_size=10,
                font_family=font_fam_sp,
                font=dict(color='navy', size=12)),
        cells=dict(values=[df_y_mayor.Candidate, df_y_mayor.Party, df_y_mayor.Age, df_y_mayor.Sex, df_y_mayor.Career, df_y_mayor.edu, df_y_mayor.wel, 
                           df_y_mayor.city, df_y_mayor.other, df_y_mayor.Vote_num, df_y_mayor.Vote, df_y_mayor.Vote_num_p, 
                           df_y_mayor.Vote_p],
               fill_color=[np.array(colors)[list(map(int, df_y_mayor.Result))]]*13,
               align='left',
               font=dict(color='black', size=12, family=font_fam_sp))))


    fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="2022 第6回市議会議員選挙",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False, False, False, False, False, False, False]},
                           {"title": "<b>6th City Council Election 2022</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2018 第5回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False, False, False, False, False, False, False]},
                           {"title": "<b>5th City Council Election 2018</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2014 第4回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False, False, False, False, False, False, False]},
                           {"title": "<b>4th City Council Election 2014</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2010 第3回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False, False, False, False, False, False, False]},
                           {"title": "<b>3rd City Council Election 2010</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2006 第2回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False, False, False, False, False, False, False]},
                           {"title": "<b>2nd City Council Election 2006</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2002 第1回市議会議員選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True, False, False, False, False, False, False]},
                           {"title": "<b>1st City Council Election 2002</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2021 第6回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, False, False, False, False, False]},
                           {"title": "<b>6th Mayor Election 2021</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2017 第5回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, True, False, False, False, False]},
                           {"title": "<b>5th Mayor Election 2017</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2013 第4回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, True, False, False, False]},
                           {"title": "<b>4th Mayor Election 2013</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2009 第3回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, True, False, False]},
                           {"title": "<b>3rd City Council Election 2010</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2005 第2回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, False, True, False]},
                           {"title": "<b>2nd Mayor Election 2005</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="2001 第1回市長選挙",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, False, False, True]},
                           {"title": "<b>1st Mayor Election 2001</b>", 'font':{'family':font_fam_sp}}])
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

    fig.update_layout(paper_bgcolor="#d9e3f1",
    width=1180,
    height=500,
    autosize=False,
    margin=dict(t=0, b=0, l=0, r=0),
    template="plotly_white",
    )

    fig.update_layout(title='<b>Choose a year</b>', title_font={'family':font_fam_sp})

    return fig

def vote_rate_council_mayor_general(df, n):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    if n==1:
        bgcolor = '#d9e3f1'
    else:
        bgcolor = '#d9e3f1'
    
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
                           {"title": "<b>Vote Rate and number of City council election</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="Mayor",
                     method="update",
                     args=[{"visible": [False, False, True, True]},
                           {"title": "<b>Vote Rate and number of Mayor election</b>", 'font':{'family':font_fam_sp}}]),
                dict(label="City Council & Mayor",
                     method="update",
                     args=[{"visible": [True, True, True, True]},
                           {"title": "<b>Vote Rate and number of City council election and Mayor election</b>", 'font':{'family':font_fam_sp}}])
                
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
    
    fig.update_layout(title_text="<b>Choose a year</b>", xaxis_title='Year', title_font={'family':font_fam_sp})
    fig.update_yaxes(title_text="Vote Rate", secondary_y=True, title_font={'family':font_fam_sp})
    fig.update_yaxes(title_text="Vote Number", secondary_y=False, title_font={'family':font_fam_sp})
    
    fig.update_layout(
    dragmode="select", hovermode='closest', clickmode='select', template='plotly_white')
    
    return fig

def result_general(df, n):
    fig = go.Figure()
    
    if n==1:
        bgcolor = '#d9e3f1'
    else:
        bgcolor = '#d9e3f1'
        
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
                           {"title": "<b>Distribution of Result across candidates {}</b>".format(year), 'font':{'family':font_fam_sp}}])
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
    
    fig.update_layout(title_text="<b>Choose a year</b>", template='plotly_white', title_font={'family':font_fam_sp})
    
    return fig     

def sex_general(df, n):
    fig = go.Figure()
    
    if n==1:
        bgcolor = '#d9e3f1'
    else:
        bgcolor = '#d9e3f1'
        
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
                           {"title": "<b>Distribution of Sex across candidates {}</b>".format(year), 'font':{'family':font_fam_sp}}])
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
    
    fig.update_layout(title_text="<b>Choose a year</b>", template='plotly_white', title_font={'family':font_fam_sp})
    
    return fig 

def party_across_year_general(df, n):
    fig = go.Figure()
    if n==1:
        bgcolor = '#d9e3f1'
    else:
        bgcolor = '#d9e3f1'
        
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

    fig.update_layout(title_text="<b>Choose a year</b>", template='plotly_white', title_font={'family':font_fam_sp})
    
    return fig

def age_general(df, n):
    fig = go.Figure()
    if n==1:
        bgcolor = '#d9e3f1'
    else:
        bgcolor = '#d9e3f1'
        
    button_list = []
    for i, year in enumerate(df[df['Type']=='市議']['Year'].unique()):
        all_f = [False]*len(df[df['Type']=='市議']['Year'].unique())
        all_f[i] = True
        
        fig.add_trace(go.Box(x=df[(df['Type']=='市議')&(df['Year']==year)]['Sex'], 
                             y=df[(df['Type']=='市議')&(df['Year']==year)]['Age'], name='{}'.format(year)))

        button = dict(label="{}".format(year),
                     method="update",
                     args=[{"visible": all_f},
                           {"title": "<b>Distribution of Age across candidates {}</b>".format(year), 'font':{'family':font_fam_sp}}])
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

    fig.update_layout(title_text="<b>Choose a year</b>", template = 'plotly_white', title_font={'family':font_fam_sp})

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
        '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])),
        Tickfont={'family':font_fam_sp})

        sex_dim = go.parcats.Dimension(values=df_y['Sex'], label="SEX", Tickfont={'family':font_fam_sp})

        party_dim = go.parcats.Dimension(values=df_y['Party'], label="PARTY", Tickfont={'family':font_fam_sp})

        votedrate_dim = go.parcats.Dimension(
        values=df_y['Vote_new'], label="VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
        ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, 
                                                                                   votedrate_min+2*dvr), 
        '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, 
                                                                                 votedrate_min+4*dvr), 
        '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[1])),
        Tickfont={'family':font_fam_sp})

        votedratef_dim = go.parcats.Dimension(
        values=df_y['Vote_p_new'], label="PREVIOUS VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[2])),
        ticktext=list(compress(['{}-{}'.format(votedratef_min, votedratef_min+dvrf), '{}-{}'.format(votedratef_min+dvrf, 
                                                                                      votedratef_min+2*dvrf), 
        '{}-{}'.format(votedratef_min+2*dvrf, votedratef_min+3*dvrf), '{}-{}'.format(votedratef_min+3*dvrf, 
                                                                                     votedratef_min+4*dvrf), 
        '{}-{}'.format(votedratef_min+4*dvrf, votedratef_min+5*dvrf)], counts_ln[2])),
        Tickfont={'family':font_fam_sp})

        if 0 in df_y['Result_p'].unique() and 1 in df_y['Result_p'].unique():

            electedf_dim = go.parcats.Dimension(values=df_y['Result_p'], label='PREVIOUS RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'], Tickfont={'family':font_fam_sp})
        if 0 not in df_y['Result_p'].unique():
            
            electedf_dim = go.parcats.Dimension(values=df_y['Result_p'], label='PREVIOUS RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'], Tickfont={'family':font_fam_sp})
        if 1 not in df_y['Result_p'].unique():
            
            electedf_dim = go.parcats.Dimension(values=df_y['Result_p'], label='PREVIOUS RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'], Tickfont={'family':font_fam_sp})

        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'], Tickfont={'family':font_fam_sp})
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'], Tickfont={'family':font_fam_sp})
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'], Tickfont={'family':font_fam_sp})

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
        {"title": "<b>Relation between multiple variables and whether they were elected {}</b>".format(df[df['Type']=='市議']['Year'].unique()[i]),
        'font':{'family':font_fam_sp}}]))
    
    fig.update_layout(paper_bgcolor="#d9e3f1",
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
        '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[1])),
        Tickfont={'family':font_fam_sp})

        votedratef_dim = go.parcats.Dimension(
        values=df_y['Vote_p_new'], label="PREVIOUS VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[2])),
        ticktext=list(compress(['{}-{}'.format(votedratef_min, votedratef_min+dvrf), '{}-{}'.format(votedratef_min+dvrf, 
                                                                                      votedratef_min+2*dvrf), 
        '{}-{}'.format(votedratef_min+2*dvrf, votedratef_min+3*dvrf), '{}-{}'.format(votedratef_min+3*dvrf, 
                                                                                     votedratef_min+4*dvrf), 
        '{}-{}'.format(votedratef_min+4*dvrf, votedratef_min+5*dvrf)], counts_ln[2])),
        Tickfont={'family':font_fam_sp})

        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'], Tickfont={'family':font_fam_sp})
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'], Tickfont={'family':font_fam_sp})
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'], Tickfont={'family':font_fam_sp})

        full_ats = [age_dim, sex_dim, party_dim, votedrate_dim, votedratef_dim, elected_dim]

        color = df_y['Result']
        colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

        fig.add_trace(go.Parcats(dimensions=full_ats,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': font_fam_sp},
                  tickfont={'size': 13, 'family': font_fam_sp},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'}))
    
    dict_list = []
    
    for i in range(len(yunique)):
        dict_list.append(dict(
        label="{}".format(yunique[i]),
        method="update",
        args=[{"visible": buttons_tf[i]},
        {"title": "<b>Relation between multiple variables and whether they were elected {}</b>".format(df[df['Type']=='市議']['Year'].unique()[i]), 
         'font':{'family':font_fam_sp}}]))
    
    fig.update_layout(paper_bgcolor="#d9e3f1",
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
        '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])),
                                      Tickfont={'family':font_fam_sp})

        sex_dim = go.parcats.Dimension(values=df_y['Sex'], label="SEX", Tickfont={'family':font_fam_sp})

        party_dim = go.parcats.Dimension(values=df_y['Party'], label="PARTY", Tickfont={'family':font_fam_sp})

        votedrate_dim = go.parcats.Dimension(
        values=df_y['Vote_new'], label="VOTE(%)", categoryorder='array', categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
        ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, 
                                                                                   votedrate_min+2*dvr), 
        '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, 
                                                                                 votedrate_min+4*dvr), 
        '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[1])), Tickfont={'family':font_fam_sp})

        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'], Tickfont={'family':font_fam_sp})
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'], Tickfont={'family':font_fam_sp})
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'], Tickfont={'family':font_fam_sp})

        full_ats = [age_dim, sex_dim, party_dim, votedrate_dim, elected_dim]

        color = df_y['Result']
        colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

        fig.add_trace(go.Parcats(dimensions=full_ats,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': font_fam_sp},
                  tickfont={'size': 13, 'family': font_fam_sp},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'}))
    
    dict_list = []
    
    for i in range(len(yunique)):
        dict_list.append(dict(
        label="{}".format(yunique[i]),
        method="update",
        args=[{"visible": buttons_tf[i]},
        {"title": "<b>Relation between multiple variables and whether they were elected {}</b>".format(df[df['Type']=='市議']['Year'].unique()[i]),
        'font':{'family':font_fam_sp}}]))
    
    fig.update_layout(paper_bgcolor="#d9e3f1",
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
        '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])), Tickfont={'family':font_fam_sp})

        sex_dim = go.parcats.Dimension(values=df_y['Sex'], label="SEX", Tickfont={'family':font_fam_sp})

        party_dim = go.parcats.Dimension(values=df_y['Party'], label="PARTY", Tickfont={'family':font_fam_sp})
        
        if 0 in df_y['Result'].unique() and 1 in df_y['Result'].unique():

            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0, 1], 
                                       ticktext=['Not elected', 'Elected'], Tickfont={'family':font_fam_sp})
        if 0 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[1], 
                                       ticktext=['Elected'], Tickfont={'family':font_fam_sp})
        if 1 not in df_y['Result'].unique():
            
            elected_dim = go.parcats.Dimension(values=df_y['Result'], label='RESULT', categoryorder = 'array', categoryarray=[0], 
                                       ticktext=['Not Elected'], Tickfont={'family':font_fam_sp})    
        

        full_ats = [age_dim, sex_dim, party_dim, elected_dim]

        color = df_y['Result']
        colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']]

        fig.add_trace(go.Parcats(dimensions=full_ats,            
                  hoveron='color', hoverinfo='count+probability',
                  labelfont={'size': 15, 'family': font_fam_sp},
                  tickfont={'size': 13, 'family': font_fam_sp},
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
        {"title": title, 'font':{'family':font_fam_sp}}]))
    
    fig.update_layout(paper_bgcolor="#d9e3f1",
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


layout = html.Div([html.Br(),
                html.Div(html.H1('POLITICS', 
                        style={'textAlign':'left', 'color':'midnightblue', 'font-size':30})
                        ),
                html.Div('西東京市の政治についての分析を見る。ほかの自治体の政治を分析する。それらの分析結果を、各種プラットフォームに応用可能な形でダウンロードする。'
                         ,
                style=
                {'font-family':'游明朝', 'textAlign':'left', 'color':'blue', 'font-size':20}),
                html.Br(),
                html.Br(),
                html.Div(
            [
               dbc.Button(
                    "ABOUT",
                    id="about-offcanvas-scrollable",
                   n_clicks=0, style={'color':'navy'}
               ),
               dbc.Offcanvas(
                    [html.Hr(), html.P(
                    "A resource for visualizing your city's data and\ngetting excited about city council election,\ndesigned mainly for Nishi Tokyo City, Tokyo,\nbut can be applied to any other city."
                    , style={'color':'navy'}),
                     html.P("-Figures on elections held in Nishi Tokyo City", style={'color':'navy'}), 
                     html.P("-Quick review on Nishi Tokyo City Council", style={'color':'navy'}), 
                     html.P("-Uploading your city's data and getting figures out", style={'color':'navy'}), 
                     html.P("-Downloading the figures as JSON files to embed them in your city home page", 
                            style={'color':'navy'}), 
                     html.Br(),
                    dcc.Markdown('''
                    **Contact : westt.sskry(at)gmail.com**
                    ''', style={'color':'navy'})],
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
                  dbc.Button('?', className="btn btn-outline-info custom-button", n_clicks=0, id='doc_button1')
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
            ''', style={'color':'navy'})), html.P([html.B('Source', style={'color':'navy'}), dcc.Markdown('''
            https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html
            ''', style={'color':'navy'})])])],
            color='info', outline = True),
            id='doc1',
            is_open=False,
        )),
        html.Br(),
        html.Br(),
        html.Div(dbc.Tabs([
        dbc.Tab(label='PARTY', tab_id='party', id = 'party_', 
            children=[
            dcc.Graph(
                figure=party_across_year_general(df, 1), id='party_graph')
        ], style={'color':'navy'}),
        dbc.Tab(label='SEX', tab_id='sex', id = 'sex_', 
                children=[
            dcc.Graph(figure=sex_general(df, 1), id='sex_graph'
            )
        ], style={'color':'navy'}),
        dbc.Tab(label='AGE', tab_id='age', id = 'age_', 
                children=[
            dcc.Graph(
                figure=age_general(df, 1), id='age_graph'
            )
        ], style={'color':'navy'}),
        dbc.Tab(label='VOTE RATE', tab_id='voterate', id = 'voterate_', 
                children=[
            dcc.Graph(
                figure=vote_rate_council_mayor_general(df_vote_rate, 1), id='vr_graph'
            )
        ], style={'color':'navy'}),
        dbc.Tab(label='RESULT', tab_id='result', id = 'result_', 
                children=[
            dcc.Graph(
                figure=result_general(df, 1), id='result_graph'
            )
        ], style={'color':'navy'})
    ], id='tabs-basic-politics')
    ),
    html.Div(id="graph-data-basic-politics", style={"display": "none"}),
    html.Br(),
    html.Br(),     
    dbc.Button("Download This Figure as a JSON File", id="btn-download-basic-politics", style={'color':'navy'}),
    dcc.Download(id="download-basic-politics"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('Candidates Name, Pledges and other info', 
                               style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
             dbc.Button('?', className="btn btn-outline-info custom-button", n_clicks=0, id='doc_button2')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('TABLE DESCRIPTION', style={'color':'navy'}),
            dbc.CardBody([
            html.P(dcc.Markdown('''
            *Pledges, Career*: Extracted from Election Gazetta of each candidate. 
            
            (*i.e* these could be reflecting editor's bias) 
            
            Candidates whose columns are highlighted in pink were elected and in blue not."
            ''', style={'color':'navy'})), html.P([html.B('Source', style={'color':'navy'}), dcc.Markdown('''
            https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html
            ''', style={'color':'navy'})])])],
            color='dark', outline = True),
            id='doc2',
            is_open=False,
        )),
    html.Br(),
    html.Br(),
    html.Div(dbc.Spinner(dcc.Graph(figure = candidate_info(df_table), id='table-politics'), color='dark')),
    html.Div(id="graph-data-table-politics", style={"display": "none"}),
    html.Br(),
    html.Br(),     
    dbc.Button("Download This Figure as a JSON File", id="btn-download-table-politics", style={'color':'navy'}),
    dcc.Download(id="download-table-politics"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('Relationship between multiple attributes and the Election Result', 
                      style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}), 
             dbc.Button('?', className="btn btn-outline-info custom-button", n_clicks=0, id='doc_button3')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('GRAPH DESCRIPTION', style={'color':'navy'}),
            dbc.CardBody([
            html.P( 
            dcc.Markdown('''
            > Each rectangle corresponds to a discrete value taken on by that variable. 
            > The relative heights of the rectangles reflect the relative frequency of 
            > occurrence of the corresponding value.
            > Combinations of category rectangles across dimensions are connected by ribbons, 
            > where the height of the ribbon corresponds to the relative frequency of 
            > occurrence of the combination of categories in the data set.

            [(Plotly Official Document)](https://plotly.com/python/parallel-categories-diagram/)
            
            Ribbons highlighted in green are those of candidates elected.
            
            *PREVIOUS VOTE/ VOTE(%)/ RESULT*: 
            If a candidate hasn't run for the previous election, 0/ Not Elected was assigned for them.
            ''', style={'color':'navy'})), html.P([html.B('Source', style={'color':'navy'}), dcc.Markdown('''
            https://www.city.nishitokyo.lg.jp/siseizyoho/senkyo/kekka/index.html
            ''', style={'color':'navy'})])])],
            color='secondary', outline = True),
            id='doc3',
            is_open=False,
        )),
    html.Br(),
    html.Br(),
    html.Div(dbc.Card(
        dbc.CardBody([dbc.Col([
                  dbc.Row(html.H3('SET VALUES', className="card-title", style={'color':'white', 'font-size':'16px'})),
                  dbc.Row(
                  children=[
                            dcc.Markdown('''Choose a year''', style={'color':'white', 'font-size':'16px'}), 
                            html.Div(dcc.Dropdown([2022, 2018, 2014, 2010, 2006, 2002], value=2022, id='input-year', 
                                                  clearable=False, className='dropdown'))]), 
                  dbc.Row(children=[dcc.Markdown('''Choose Attributes''', style={'color':'white', 'font-size':'16px'}), 
                          dcc.Checklist(['AGE', 'SEX', 'PARTY', 'VOTE', 'VOTE(%)', 
                                         'PREVIOUS VOTE', 'PREVIOUS VOTE(%)', 'PREVIOUS RESULT'], 
                                    id='attributes', style = {'display': 'flex', 'color':'white'}
                 )])
              ])
            ]), className='set-value-card', color='info'
          )
         ),
    html.Div(dbc.Button(id='submit-button-state1', n_clicks=0, children='Select Values', color='info', 
                        style={'color':'navy'})),
    html.Br(),
    html.Div(id='selection_completed'),
    html.Br(),
    html.Div(dcc.Graph(id='parcat')),
    html.Div(id="graph-data-parcat-politics", style={"display": "none"}),
    html.Br(),
    html.Br(),     
    dbc.Button("Download This Figure as a JSON File", id="btn-download-parcat-politics", style={'color':'navy'}),
    dcc.Download(id="download-parcat-politics"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('City Council Review', style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
             dbc.Button('?', className="btn btn-outline-info custom-button", n_clicks=0, id='doc_button5')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('GRAPH DESCRIPTION', style={'color':'navy'}),
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
             [scikit-learn text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
             
             -Top 100 nouns regarding the tf-idf score were extracted.  
             
             *2. Coocurrance network graph calculation*
             
             -On the 100 nouns, algorithmns for `NetworkX` was performed.
             [NetworkX documentation](https://networkx.org/documentation/stable/reference/algorithms/index.html)
            
            ''', style={'color':'navy'})), html.P([html.B('Source', style={'color':'navy'}), html.Div(dcc.Markdown(
                '''
                https://www.city.nishitokyo.tokyo.dbsr.jp/index.php/
                ''', style={'color':'navy'}))])])],
            color='dark', outline = True),
            id='doc5',
            is_open=False,
        )),
    html.Br(),
    html.Br(),
    html.Div(dbc.Card(dbc.CardBody([dbc.Col([
        dbc.Row(html.H3('SET VALUES', className="card-title", style={'color':'white', 'font-size':'16px'})),
        dbc.Row(children=[dcc.Markdown('''Choose a year''', style={'color':'white', 'font-size':'16px'}), 
                          html.Div(dcc.Dropdown([y for y in reversed(range(2001, 2023))], 
    value=2022, id='input-year-network', clearable=False, className='dropdown'))
             ])
       ])
      ]), className='set-value-card', color='info'
    )),
    html.Br(),
    html.Div([html.Br(), dbc.Spinner(dcc.Graph(id = 'network'), color='dark')]),
    html.Div(id="graph-data-network-politics", style={"display": "none"}),
    html.Br(),
    html.Br(),     
    dbc.Button("Download This Figure as a JSON File", id="btn-download-network-politics", style={'color':'navy'}),
    dcc.Download(id="download-network-politics"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([html.H2('Make graphs of your city!', style={'textAlign': 'center', 'color': 'navy', 'font-size': 30}),
             dbc.Button('?', className="btn btn-outline-info custom-button", n_clicks=0, id='doc_button4')]),
    html.Div(dbc.Collapse(
            dbc.Card([dbc.CardHeader('DESCRIPTION', style={'color':'navy'}),
            dbc.CardBody([html.P(dcc.Markdown('''
            By uploading csv files, you can obtain figures. File format restriction is strict. 
            Please see below for the info.
            ''', style={'color':'navy'}))])],
            color='primary', outline = True),
            id='doc4',
            is_open=False,
        )),
    html.Br(),
    html.Br(),
    html.H3('Basic Statistical Figures', style={'textAlign': 'left', 'color': 'navy', 'font-size': 20}),
    
    html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',html.A('Select a CSV File')
        ]),
        className='upload-box-style',
        multiple=False
    )]),
    
    html.H3('Your Graphs:', style={'font-size':20}),
    html.Br(),
    html.Div(id='output-data-upload'),
    html.Div(id="graph-data-basic-politics-upload", style={"display": "none"}),
    html.Br(),
    html.Br(),
    html.Div(id='download-button-turn-up'),
    html.Br(),
    html.Br(),
    html.H3('Relationship between multiple attributes and the Election Result', 
            style={'textAlign': 'left', 'color': 'navy', 'font-size': 20}),
    
    html.Div([
    dcc.Upload(
        id='upload-data2',
        children=html.Div(['Drag and Drop or ',html.A('Select a CSV File')
        ]),
        className='upload-box-style',
        multiple=False
    )]),
    
    html.H3('Your Graphs:', style={'font-size':20, 'color':'navy'}),
    html.Br(),
    html.Div([
        dbc.Tabs([
            dbc.Tab(tab_id='set 1', id = 'set 1_', style={'color':'navy'}, 
            label='SET 1', children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")], id='badge_1')
        ]),
        dbc.Tab(tab_id='set 2', id = 'set 2_', label='SET 2', style={'color':'navy'},
                children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")
            , dbc.Badge('VOTE(%)', text_color="dark", color="light")], id='badge_2')
        ]),
        dbc.Tab(tab_id='set 3', id = 'set 3_', label='SET 3', style={'color':'navy'},
                children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")
            , dbc.Badge('VOTE(%)', text_color="dark", color="light"),
            dbc.Badge('PREVIOUS VOTE(%)', text_color="dark", color="light")], id='badge_3')
        ]),
        dbc.Tab(tab_id='set 4', id = 'set 4_', label='SET 4', style={'color':'navy'},
                children=[html.Br(),
            html.Span([dbc.Badge('AGE', text_color="dark", color="light")
            , dbc.Badge('SEX', text_color="dark", color="light"),
            dbc.Badge('PARTY', text_color="dark", color="light")
            , dbc.Badge('VOTE(%)', text_color="dark", color="light"),
            dbc.Badge('PREVIOUS VOTE(%)', text_color="dark", color="light"),
            dbc.Badge('PREVIOUS RESULT', text_color="dark", color="light")], id='badge_4')
        ])
    ], id='upload2_tabs')
    ]), 
    html.Br(), dbc.Button(id='submit-button-state2', n_clicks=0, children='Change Sets', color='info'),
    html.Div(id='selection_completed2'),
    html.Div(id = 'upload2_set'),
    html.Div(id="graph-data-parcat-upload", style={"display": "none"}),
    html.Br(),
    html.Br(),
    html.Div(id='parcat-download-button-turn-up'),
    html.Br(),
    html.Br(),
    html.H3('Upload File Format', style={'color':'navy'}),
    html.Br(),
    html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [html.P([html.B("File Type", style={'color':'navy'}),html.Div("-CSV", style={'color':'navy'})]), 
                 html.P([html.B("Encoding", style={'color':'navy'}), html.Div("-Shift JIS", style={'color':'navy'})]), 
                 html.P([html.B("Columns", style={'color':'navy'}),dcc.Markdown('''
                *-Age* (Age of a candidate)
                
                *-Sex* (Sex of a candidate, Male or Female)
                
                *-Year* (Year when the candidate ran for the election)
                
                *-Party* (A party a candidate belongs to)
                
                *-Vote_rate* (Vote rate of the election)
                
                *-Electrates* (Number of electrates in the election)
                
                *-Type* (Election type, 市議or市長)
                
                *-Result* (Whether the candidate were elected, 1 for elected, 0 for not)
                
                *-Candidate:optional* (Name of a candidate)
                 ''', style={'color':'navy'})]),
                html.P([html.B("Note", style={'color':'navy'}), 
                        html.Div("-Columns which have nulls (NaNs, N/As) are deleted automatically", style={'color':'navy'})])]
                , title="Basic Statistical Figures"
            ),
            dbc.AccordionItem([html.P([html.B("File Type", style={'color':'navy'}), html.Div("-CSV", style={'color':'navy'})]), 
                               html.P([html.B("Encoding", style={'color':'navy'}),html.Div("-Shift JIS", style={'color':'navy'})]), 
                               html.P([html.B("Columns", style={'color':'navy'}), dcc.Markdown('''
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
                ''', style={'color':'navy'})]), 
                html.P([html.B("Note", style={'color':'navy'}), html.Div("-Columns which have nulls (NaNs, N/As) are deleted automatically")])]
                , title="Relationship between multiple attributes and the Election Result", style={'color':'navy'})
            ,
                 ],
                 flush=True,
                 start_collapsed=True,
             ),
        ),
    html.Br(),
    html.Br(),
    html.H3('About the Downloaded Files', style={'color':'navy'}),
    html.Br(),
    html.Div(dbc.Accordion([dbc.AccordionItem([html.P([html.B('File Format', style={'color':'navy'}), 
                                                       html.Div('-JSON (stringified)', style={'color':'navy'})])]),
                           dbc.AccordionItem([html.P([html.B('Term of Use (利用について)', style={'color':'navy'}), 
                                                      html.Div('-Can be used for any purposes other than commercial use. (商用利用以外であれば、ご自由に利用いただけます。)', 
                                                               style={'color':'navy'})])])], 
                           flush=True,start_collapsed=True)),
    html.Br(),
    html.Div(
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='assets/github_mark.png', height=15, alt='Github Official Logo'), width="auto"),
                            dbc.Col("Github", style={'font-size': '12px', 'textAlign': 'center', 'color': 'mintcream'}),
                        ],
                        align="center",
                        className="align-items-center",
                    ),
                    href='https://github.com/Kyoko-Tachibana/Learning-about-City-from-Data_-Machi-Learn-',
                )
            )
        ],
        brand='This page uses Dash, is themed by Bootstrap.Morph, and is deployed by Render.',
        brand_style={'font-size': '12px', 'textAlign': 'center', 'color': 'mintcream', 'font': 'italic'},
        color='info',
        dark=True,
        sticky='bottom',
        style={'height': '5vh', 'width': '100vw'},
    )
)

    

], lang="en", className='main-page-layout')


# In[ ]:

@callback(
    Output("graph-data-network-politics", "children"),
    Input('network', "figure"),
    prevent_initial_call=True
)
def store_network_data(network_figure):
    try:
        return json.dumps(network_figure, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("download-network-politics", "data"),
    Input("btn-download-network-politics", "n_clicks"),
    State("graph-data-network-politics", "children"),
    prevent_initial_call=True,
)
def download_network_structure(n_clicks, network_structure_json):
    try:
        if n_clicks is None or not network_structure_json:
            raise PreventUpdate

        stored_network_structure = json.loads(network_structure_json)
        content_string = json.dumps(stored_network_structure)

        file_content = {
        "filename": "council_politics_nishitokyo.json",
        "content": content_string,
        "type": "application/json",
    }
        return file_content
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("graph-data-parcat-politics", "children"),
    Input('parcat', "figure"),
    prevent_initial_call=True
)
def store_parcat_data(parcat_figure):
    try:
        return json.dumps(parcat_figure, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("download-parcat-politics", "data"),
    Input("btn-download-parcat-politics", "n_clicks"),
    State("graph-data-parcat-politics", "children"),
    prevent_initial_call=True,
)
def download_parcat_structure(n_clicks, parcat_structure_json):
    try:
        if n_clicks is None or not parcat_structure_json:
            raise PreventUpdate

        stored_parcat_structure = json.loads(parcat_structure_json)
        content_string = json.dumps(stored_parcat_structure)

        file_content = {
        "filename": "relation_politics_nishitokyo.json",
        "content": content_string,
        "type": "application/json",
    }
        return file_content
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("graph-data-table-politics", "children"),
    Input('table-politics', "figure"),
    prevent_initial_call=True
)
def store_table_data(table_figure):
    try:
        return json.dumps(table_figure, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("download-table-politics", "data"),
    Input("btn-download-table-politics", "n_clicks"),
    State("graph-data-table-politics", "children"),
    prevent_initial_call=True,
)
def download_table_structure(n_clicks, table_structure_json):
    try:
        if n_clicks is None or not table_structure_json:
            raise PreventUpdate

        stored_table_structure = json.loads(table_structure_json)
        content_string = json.dumps(stored_table_structure)

        file_content = {
        "filename": "table_politics_nishitokyo.json",
        "content": content_string,
        "type": "application/json",
    }
        return file_content
    except Exception as e:
        print(e)
        raise PreventUpdate


@callback(Output('download-button-turn-up', 'children'),
         Input('output-data-upload', 'children'),
         prevent_initial_call=True)

def turnup_download_button(yourgraph):
    try:
        if yourgraph is not None:
            return [dbc.Button("Download This Figure as a JSON File", id="btn-download-basic-politics-upload", 
                               style={'color':'navy'}),
    dcc.Download(id="download-basic-politics-upload")]
    
        else:
            raise PreventUpdate
    except Exception as e:
        print(e)
        raise PreventUpdate
        

@callback(
    Output("graph-data-basic-politics-upload", "children"),
    Input('output-data-upload', "children"),
    prevent_initial_call=True,
)
def store_graph_data2(graph_children):
    try:
        return json.dumps(graph_children, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("download-basic-politics-upload", "data"),
    Input("btn-download-basic-politics-upload", "n_clicks"),
    State("graph-data-basic-politics-upload", "children"),
    prevent_initial_call=True,
)
def download_tabs_structure2(n_clicks, tabs_structure_json):
    try:
        if n_clicks is None or not tabs_structure_json:
            raise PreventUpdate

        stored_tabs_structure = json.loads(tabs_structure_json)
        content_string = json.dumps(stored_tabs_structure)

        file_content = {
        "filename": "basic_politics_your_city.json",
        "content": content_string,
        "type": "application/json",
    }
        return file_content
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(Output('parcat-download-button-turn-up', 'children'),
         Input('upload2_set', 'figure'),
         prevent_initial_call=True)

def turnup_download_button_parcat(yourgraph):
    try:
        if yourgraph is not None:
            return [dbc.Button("Download This Figure as a JSON File", id="btn-download-parcat-upload", 
                               style={'color':'navy'}),
    dcc.Download(id="download-parcat-upload")]
    
        else:
            raise PreventUpdate
    except Exception as e:
        print(e)
        raise PreventUpdate  

@callback(
    Output("graph-data-parcat-upload", "children"),
    Input('upload2_set', "figure"),
    prevent_initial_call=True,
)
def store_graph_data3(graph_children):
    try:
        return json.dumps(graph_children, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("download-parcat-upload", "data"),
    Input("btn-download-parcat-upload", "n_clicks"),
    State("graph-data-parcat-upload", "children"),
    prevent_initial_call=True,
)
def download_parcat(n_clicks, parcat_json):
    try:
        if n_clicks is None or not parcat_json:
            raise PreventUpdate

        parcat_structure = json.loads(parcat_json)
        content_string = json.dumps(parcat_structure)

        file_content = {
        "filename": "relation_your_city.json",
        "content": content_string,
        "type": "application/json",
    }
        return file_content
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("graph-data-basic-politics", "children"),
    Input('tabs-basic-politics', "children"),
    prevent_initial_call=True
)
def store_graph_data(tabs_children):
    try:
        return json.dumps(tabs_children, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print(e)
        raise PreventUpdate

@callback(
    Output("download-basic-politics", "data"),
    Input("btn-download-basic-politics", "n_clicks"),
    State("graph-data-basic-politics", "children"),
    prevent_initial_call=True,
)
def download_tabs_structure(n_clicks, tabs_structure_json):
    try:
        if n_clicks is None or not tabs_structure_json:
            raise PreventUpdate

        stored_tabs_structure = json.loads(tabs_structure_json)
        content_string = json.dumps(stored_tabs_structure)

        file_content = {
        "filename": "basic_politics_nishitokyo.json",
        "content": content_string,
        "type": "application/json",
    }
        return file_content
    except Exception as e:
        print(e)
        raise PreventUpdate

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
    return html.Div(
        dbc.Tabs([
        dbc.Tab(label='Party', children=[html.Br(),
            dcc.Graph(
                figure=party_across_year_general(df_in, 0))
        ]),
        dbc.Tab(label='Sex', children=[html.Br(),
            dcc.Graph(figure=sex_general(df_in, 0)
            )
        ]),
        dbc.Tab(label='Age', children=[html.Br(),
            dcc.Graph(
                figure=age_general(df_in, 0)
            )
        ]),
        dbc.Tab(label='Vote Rate', children=[html.Br(),
            dcc.Graph(
                figure=vote_rate_council_mayor_general(df_in, 0)
            )
        ]),
        dbc.Tab(label='Result', children=[html.Br(),
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
                     '{}-{}'.format(age_min+4*da, age_min+5*da)], counts_ln[0])),
                                          Tickfont={'family':font_fam_sp})

            sex_dim = go.parcats.Dimension(values=df['Sex'], label="SEX", Tickfont={'family':font_fam_sp})

            party_dim = go.parcats.Dimension(values=df['Party'], label="PARTY", Tickfont={'family':font_fam_sp})
 
            vote_dim = go.parcats.Dimension(values=df['Vote_num_new'], label='VOTE', categoryorder='array', 
                      categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[1])),
                      ticktext=list(compress(['{}-{}'.format(vote_min, vote_min+dv), '{}-{}'.format(vote_min+dv, vote_min+2*dv), 
                      '{}-{}'.format(vote_min+2*dv, vote_min+3*dv), '{}-{}'.format(vote_min+3*dv, vote_min+4*dv), 
                      '{}-{}'.format(vote_min+4*dv, vote_min+5*dv)], counts_ln[1])),
                                           Tickfont={'family':font_fam_sp})

            votedrate_dim = go.parcats.Dimension(values=df['Vote_new'], label="VOTE(%)", categoryorder='array', 
                           categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[2])),
                           ticktext=list(compress(['{}-{}'.format(votedrate_min, votedrate_min+dvr), '{}-{}'.format(votedrate_min+dvr, votedrate_min+2*dvr), 
                           '{}-{}'.format(votedrate_min+2*dvr, votedrate_min+3*dvr), '{}-{}'.format(votedrate_min+3*dvr, votedrate_min+4*dvr), 
                           '{}-{}'.format(votedrate_min+4*dvr, votedrate_min+5*dvr)], counts_ln[2])),
                                                Tickfont={'family':font_fam_sp})

            votef_dim = go.parcats.Dimension(values=df['Vote_num_p_new'], label='PREVIOUS VOTE', categoryorder='array', 
                       categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[3])),
                       ticktext=list(compress(['{}-{}'.format(votef_min, votef_min+dvf), '{}-{}'.format(votef_min+dvf, votef_min+2*dvf), 
                       '{}-{}'.format(votef_min+2*dvf, votef_min+3*dvf), '{}-{}'.format(votef_min+3*dvf, votef_min+4*dvf), 
                       '{}-{}'.format(votef_min+4*dvf, votef_min+5*dvf)], counts_ln[3])),
                                            Tickfont={'family':font_fam_sp})

            votedratef_dim = go.parcats.Dimension(values=df['Vote_p_new'], label="PREVIOUS VOTE(%)", categoryorder='array', 
                            categoryarray=list(compress([0, 1, 2, 3, 4], counts_ln[4])),
                            ticktext=list(compress(['{}-{}'.format(votedratef_min, votedratef_min+dvrf), '{}-{}'.format(votedratef_min+dvrf, votedratef_min+2*dvrf), 
                            '{}-{}'.format(votedratef_min+2*dvrf, votedratef_min+3*dvrf), '{}-{}'.format(votedratef_min+3*dvrf, votedratef_min+4*dvrf), 
                            '{}-{}'.format(votedratef_min+4*dvrf, votedratef_min+5*dvrf)], counts_ln[4])),
                                                 Tickfont={'family':font_fam_sp})

            if 0 in df['Result_p'].unique() and 1 in df['Result_p'].unique():

                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[0, 1], categoryorder = 'array',
                          ticktext=['Not elected', 'Elected'], Tickfont={'family':font_fam_sp})
                
            if 0 not in df['Result_p'].unique():
                
                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[1], categoryorder = 'array',
                          ticktext=['Elected'], Tickfont={'family':font_fam_sp})
                
            if 1 not in df['Result_p'].unique():
                
                electedf_dim = go.parcats.Dimension(values=df['Result_p'], label='PREVIOUS RESULT', categoryarray=[0], categoryorder = 'array',
                          ticktext=['Not Elected'], Tickfont={'family':font_fam_sp})
    
            if 0 in df['Result'].unique() and 1 in df['Result'].unique():
    
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[0, 1], categoryorder = 'array',
                          ticktext=['Not elected', 'Elected'], Tickfont={'family':font_fam_sp})
        
            if 0 not in df['Result'].unique():       
                
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[1], categoryorder = 'array',
                          ticktext=['Elected'], Tickfont={'family':font_fam_sp})
                
            if 1 not in df['Result'].unique():
                
                elected_dim = go.parcats.Dimension(values=df['Result'], label='RESULT', categoryarray=[0], categoryorder = 'array',
                          ticktext=['Not Elected'], Tickfont={'family':font_fam_sp})
                
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
                  labelfont={'size': 15, 'family': font_fam_sp},
                  tickfont={'size': 13, 'family': font_fam_sp},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'})])
            
            fig.update_layout(paper_bgcolor = '#d9e3f1',
                             title = '<b>{}</b>'.format(entered_year), title_font={'family':font_fam_sp})
            
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
                  labelfont={'size': 15, 'family': font_fam_sp},
                  tickfont={'size': 13, 'family': font_fam_sp},
                  arrangement='freeform',
                  line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'})])
            
            fig.update_layout(paper_bgcolor = '#d9e3f1',
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
               Input('submit-button-state1', 'n_clicks'),
          id='parcat_at'
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




