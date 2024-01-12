#!/usr/bin/env python
# coding: utf-8

# In[3]:


from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from pages import politics, index, city


app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH], suppress_callback_exceptions=True, meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'},
        {'charset': 'utf-8'}
    ])

server = app.server
app.title = 'データで街について学べるサイト「まちラーン」'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/politics':
        return politics.layout
    
    if pathname == '/city':
        return city.layout

    else:
        return index.layout


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')


# In[ ]:




