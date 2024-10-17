import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
from datetime import date

from app import app
data_fpath = "assets/datasets/nc_utilities.csv"

def CharacteristicTimeSeries(df, start_index=2):
    radio_dict = {
        0: 'Plot one line',
        1: '(Compare utilities) Plot multiple lines',
        2: '(Compare variables) Plot multiple lines'
    }
    return [
            html.Div([
                    dbc.RadioItems(
                        id='cts-radio',
                        options=[
                            {'label': radio_dict[i], 'value': i} for i in radio_dict.keys()
                        ],
                        value=0
                    ),
                    html.Hr(),
                    html.P(id='cts-char-var-prompt', style={'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='cts-char-variable',
                        options=[
                            {'label': i, 'value': i} for i in list(df.iloc[:,1:2].squeeze().unique())
                        ]
                    ),
                    html.Br(),
                    html.P(id='cts-var-prompt', style={'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='cts-variable',
                        options=[
                            {'label': i, 'value': i} for i in df.columns[start_index:]
                        ]
                    ),
                    html.Br(),
                    html.P("Select a date range to plot:", style={'margin-bottom': '5px'}),
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        month_format="MMM Do, YY",
                        end_date_placeholder_text='MMM Do, YY',
                        min_date_allowed=date(1996, 7, 1),
                        max_date_allowed=date(2024, 8, 1),
                        start_date=date(1996, 7, 1),
                        end_date=date(2024, 8, 1)
                    ),
                    dcc.Graph(id='characteristic-time-series')],
                    className='graph')
        ]

@app.callback(
    [Output('cts-char-variable', 'multi'),
     Output('cts-char-variable', 'value'),
     Output('cts-variable', 'multi'),
     Output('cts-variable', 'value'),
     Output('cts-char-var-prompt', 'children'),
     Output('cts-var-prompt', 'children')],
    Input('cts-radio', 'value'))
def set_multi(selected_option):
    df = pd.read_csv(data_fpath, index_col=0)
    if selected_option == 0:
        return [False,
                list(df.iloc[:,1:2].squeeze().unique())[0],
                False,
                df.columns[2],
                'Select a utility:',
                'Select a variable to plot:']
    if selected_option == 1:
        return [True,
                [list(df.iloc[:,1:2].squeeze().unique())[0]],
                False,
                df.columns[2],
                'Select one or more utilities:',
                'Select a variable to plot:']
    else:
        return [False,
                list(df.iloc[:,1:2].squeeze().unique())[0],
                True,
                [df.columns[2]],
                'Select a utility:',
                'Select one or more variables to plot:']
    
@app.callback(
    Output('characteristic-time-series', 'figure'),
    Input('cts-char-variable', 'value'),
    Input('cts-variable', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def update_graph(char_variable, variable, start_date, end_date):
    if type(variable) == list:
        df = pd.read_csv(data_fpath, index_col=0).dropna(subset=variable)
    else:
        df = pd.read_csv(data_fpath, index_col=0).dropna(subset=[variable])
    char_column = df.iloc[:, 1:2].columns[0]
    if type(char_variable) == list:
        df = df[df[char_column].isin(char_variable)]
    else:
        df = df[df[char_column] == char_variable]
    reporting_period = df.columns[0]
    df = df[df[reporting_period] >= start_date]
    df = df[df[reporting_period] <= end_date]
    if type(char_variable) == list and len(char_variable) > 0:
        char_color_dict = {}
        colors = ['#636efa', 'red', 'green', 'purple', 'orange', 'teal', 'pink']
        for i in range(len(char_variable)):
            char = char_variable[i]
            char_color_dict[char] = colors[i]
            if i == 0:
                fig = px.line(df[df[char_column] == char],
                              x=df.columns[0],
                              y=variable,
                              color=df.columns[1],
                              color_discrete_map=char_color_dict)
            else:
                fig.add_traces(list(px.line(df[df[char_column] == char],
                                    x=df.columns[0],
                                    y=variable,
                                    color=df.columns[1],
                                    color_discrete_map=char_color_dict).select_traces()))
    else:
        fig = px.line(df, x=df.columns[0], y=variable)
    return fig