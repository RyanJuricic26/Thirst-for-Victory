import dash
from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name='Project Overview')

layout = html.Div(
    [
        dcc.Markdown('# Project Overview')
    ]
)