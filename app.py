import dash
from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os


external_stylesheets = [dbc.themes.CYBORG]

app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           title='Thirst for Victory',
           use_pages=True)

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"],
                         className='ms-2',
                         style={
                             'fontFamily': 'Old Standard TT',
                             'fontSize': 20
                         }),
            ],
            href=page['path'],
            active='exact',
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className='bg-light' # used for css styling
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            [
                html.Br(),
                html.Div("Thirst for Victory",
                    style={
                        'fontSize': 60,
                        'textAlign': 'center',
                        'color': '#FFFFFF',
                        'fontFamily': 'Old Standard TT'
                        })
            ]
        )
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)