import dash_core_components as dcc
import dash_html_components as html
from app import app, server
import os
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from utils.dataset_tab import Dataset
import utils.visualization_tabs as visualization
import utils.style_dicts as style

dataset = 'North Carolina Electric Utility Data (1996-2024)'
df = np.round(pd.read_csv('assets/datasets/nc_utilities.csv', index_col=0), 4)

columns = df.columns.tolist()
string_columns = [columns.index(x) for x in columns if isinstance(df[x].iloc[0], str)]
keywords = [x.casefold() for x in df.columns.tolist() + dataset.split()]
for index in string_columns:
        keywords = keywords + [x.casefold() for x in df.iloc[:, index].unique().tolist()]

dataset_desc = html.Div([html.P(['Sources: ',
                                 'North Carolina Utilities Commission (',
                                 html.A(
                                         'Docket M-100 Sub 179',
                                         href='https://starw1.ncuc.gov/NCUC/page/docket-docs/PSC/DocketDetails.aspx?DocketId=a07c0087-3679-4a21-8874-0dddaee68792',
                                         style={'text-decoration':'underline'}
                                 ),
                                 ', ',
                                 html.A(
                                         'Docket M-100 Sub 158',
                                         href='https://starw1.ncuc.gov/NCUC/page/docket-docs/PSC/DocketDetails.aspx?DocketId=66e14449-b407-4ac3-93eb-a417521e1269',
                                         style={'text-decoration':'underline'}
                                 ),
                                 '), '
                                 'U.S. Energy Information Administration (',
                                 html.A(
                                         'EIA-861M',
                                         href='https://www.eia.gov/electricity/data/eia861m/',
                                         style={'text-decoration':'underline'}
                                 ),
                                 '), ',
                                 'Indiana University Energy Justice Lab (',
                                 html.A(
                                         'Utility Disconnections Data Explorer',
                                         href='https://http-149-165-168-30-80.proxy-js2-iu.exosphere.app/',
                                         style={'text-decoration':'underline'}
                                 ),
                                 ')'
                        ]),
                       html.P('Note: All of the data here concern only residential accounts of electric services for each utility.')])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Br(),
    html.Center(html.H4(dataset, style={'font-weight': 'bold'})),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Dataset',
                children=Dataset(df, dataset_desc), style=style.data_tab, selected_style=style.data_tab_selected),
        dcc.Tab(label='Visualization',
                children=visualization.CharacteristicTimeSeries(df), style=style.data_tab, selected_style=style.data_tab_selected),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))