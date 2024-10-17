import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import dash_table

from app import app
data_fpath = "assets/datasets/nc_utilities.csv"

download = html.Div([dbc.Button(html.Strong("Download"),
                       color="info",
                       block=True,
                       id="btn_txt"),
                     dcc.Download(id="download-raw-file")])

@app.callback(
    Output("download-raw-file", "data"),
    Input("btn_txt", "n_clicks"))
def func(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        df = pd.read_csv(data_fpath, index_col=0)
        return dcc.send_data_frame(df.to_csv, filename="nc_utility_data_1996_to_2024.csv")

def Dataset(df, desc = 'Insert dataset description here.'):
    dt_columns = []
    data_types = df.dtypes
    for col in data_types.keys().tolist():
            if 'str' in str(data_types[col]):
                    dt_columns.append({'name': col, 'id': col, 'type': 'text'})
            else:
                    dt_columns.append({'name': col, 'id': col, 'type': 'numeric'})
    
    filter_instructions = "To filter the data down to rows that match a desired value for a column, type the value in the second row and press 'Enter'. Greater-than(-or-equal-to) and less-than(-or-equal-to) symbols can also be used for numeric or time-based columns (e.g., '>=2024-01-01' to display only 2024 values). Note that filtering is just for inspection and will not affect the downloaded dataset."

    data_table = html.Div([dash_table.DataTable(
        columns=dt_columns,
        data=df.to_dict('records'),
        filter_action='native',
        page_size=15,
        style_table={'overflowX': 'auto'},
        style_cell={
            'font-family': '"Open Sans", verdana, arial, sans-serif',
            'font-size': '12',
            'height': 'auto',
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        }
    )], style={'margin': '100px', 'margin-bottom': '0px', 'margin-top': '40px'})

    return [download,
            data_table,
            html.P(desc, style={'margin-top': '10px', 'margin-left': '100px', 'font-size': '16px'}),
            html.P(filter_instructions, style={'margin-left': '100px', 'margin-right': '100px', 'font-size': '16px'})]