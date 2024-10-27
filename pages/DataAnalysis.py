import dash
from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

dist = np.load('Data/Bootstrapped_Distribution.npy')
df = pd.read_csv('Data/Complete_Dataset.csv')

conf_options = [
    {'label': '90%', 'value': 90},
    {'label': '95%', 'value': 95},
    {'label': '97.5%', 'value': 97.5},
    {'label': '99%', 'value': 99}
]

dash.register_page(__name__, name='Data Analysis')

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown('### Project Analysis',
                                     style={'textAlign': 'center'}),
                    ], width = 10
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Select a Season:'),
                        html.Div([
                            dcc.Dropdown(options=conf_options,
                                         value=95,
                                         id='conf_interval',
                                         style={'backgroundColor': '#333333', 'color': '#FFFFFF'})
                        ], style={'backgroundColor': '#333333', 'color': '#FFFFFF', 'padding': '10px'})
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='seed_dist',
                                  figure={})
                    ], width=12
                )
            ]
        )
    ]
)

@callback(
    Output(component_id='seed_dist', component_property='figure'),
    Input(component_id='conf_interval', component_property='value'),
)
def update_graph(conf_interval):
    template = 'plotly_dark'
    playoff_data = df[df['SEED'] > 0]
    avg_pepsi_seed = round(playoff_data[playoff_data['SPONSOR']=='Pepsi']['SEED'].mean(),2)
    if not conf_interval:
        # Create the histogram for bootstrap_means using Plotly
        fig = go.Figure()

        # Add histogram
        fig.add_trace(go.Histogram(
            x=dist,
            nbinsx=50,  # Adjust the number of bins
            marker=dict(color='#fe001a'),
            name='Bootstrapped Distribution of Mean Seed for Coke School\'s',
            )
        )

        # Add vertical line for avg_pepsi_seed
        fig.add_vline(
            x=avg_pepsi_seed,
            line_color='#2151A1',
            line_width=3,
            annotation_text=f'Pepsi School\'s Mean Seed: {avg_pepsi_seed}',
            annotation_position='top',
            name='Pepsi School\'s Mean Seed'
        )

        # Update the layout to add title, legend, and axes labels
        fig.update_layout(
            title='Bootstrapped Distribution of Mean Seed for Coke School\'s',
            xaxis_title='Seed',
            yaxis_title='Frequency',
            showlegend=True,
            template=template
        )

        # Update traces (set border color for histogram bars)
        fig.update_traces(
            marker=dict(
                line=dict(color='black', width=1)  # Set border color and width
            )
        )
        return fig
    else:
        left_interval_endpoint = np.percentile(dist, ((100 - conf_interval) / 2))
        right_interval_endpoint = np.percentile(dist, 100 - ((100 - conf_interval)))

        int_title = round(left_interval_endpoint, 2), round(right_interval_endpoint, 2)

        # Create the histogram for bootstrap_means using Plotly
        fig = go.Figure()

        # Add histogram
        fig.add_trace(go.Histogram(
            x=dist,
            nbinsx=50,  # Adjust the number of bins
            marker=dict(color='#fe001a'),
            name='Bootstrapped Distribution of Mean Seed for Coke School\'s',
            )
        )

        # Add confidence interval (as a line or a bar)
        fig.add_trace(go.Scatter(
            x=[left_interval_endpoint, right_interval_endpoint],
            y=[0, 0],  # y-values are zero because it's a horizontal line
            mode='lines',
            line=dict(color='yellow', width=10),
            name=f'{conf_interval}% Confidence Interval: [{int_title[0]}, {int_title[1]}]'
        ))

        # Add vertical line for avg_pepsi_seed
        fig.add_vline(
            x=avg_pepsi_seed,
            line_color='#2151A1',
            line_width=3,
            annotation_text=f'Pepsi School\'s Mean Seed: {avg_pepsi_seed}',
            annotation_position='top',
            name='Pepsi School\'s Mean Seed'
        )

        # Update the layout to add title, legend, and axes labels
        fig.update_layout(
            title='Bootstrapped Distribution of Mean Seed for Coke School\'s',
            xaxis_title='Seed',
            yaxis_title='Frequency',
            showlegend=True,
            template=template
        )

        # Update traces (set border color for histogram bars)
        fig.update_traces(
            marker=dict(
                line=dict(color='black', width=1)  # Set border color and width
            )
        )
        return fig


