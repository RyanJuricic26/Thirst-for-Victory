import dash
from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__,
           external_stylesheets=[dbc.themes.CYBORG],
           title='Thirst for Victory',
           use_pages=True)

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className='ms-2'),
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
        dbc.Col(html.Div("Thirst for Victory",
                         style={'fontSize': 50, 'textAlign': 'center'}))
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

#         # Framework of the main app
#         html.Div("Thirst for Victory Project", style={'fontSize':50, 'textAlign': 'center'})
#         html.Div([
#             dcc.Link(children=page['name']+"  |  ", href=page['path'])
#             for page in Dash.page_registry.values()
#         ]),
#         html.Hr(),
#
#         # content of each page
#         Dash.page_container
#     ]
# )

if __name__ == '__main__':
    app.run(debug=True)