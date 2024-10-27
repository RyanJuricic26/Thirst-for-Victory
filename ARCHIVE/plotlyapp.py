from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Importing Data
df = pd.read_csv('Data/Complete_Dataset.csv')
df = df.drop(columns=['Unnamed: 0'])

season_options = [
    {'label': '2013-2014', 'value': 2014},
    {'label': '2014-2015', 'value': 2015},
    {'label': '2015-2016', 'value': 2016},
    {'label': '2016-2017', 'value': 2017},
    {'label': '2017-2018', 'value': 2018},
    {'label': '2018-2019', 'value': 2019},
    {'label': '2019-2020', 'value': 2020},
    {'label': '2020-2021', 'value': 2021},
    {'label': '2021-2022', 'value': 2022},
    {'label': '2022-2023', 'value': 2023},
    {'label': '2023-2024', 'value': 2024}
]

custom_colors = {
    'Coke': '#F40000',
    'Pepsi': '#0E0E96',
    'Dr. Pepper': '#890024',
    'BioSteel': '#00FF00'
}

app = Dash(__name__,
           external_stylesheets=[dbc.themes.CYBORG],
           title='Thirst for Victory')

app.layout = html.Div(
    style={'backgroundColor': '#111111', 'color': '#FFFFFF', 'padding': '20px'},
    children=[
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Markdown('# Thirst for Victory', style={'textAlign': 'center'})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label('Select a Season:'),
                    html.Div([
                        dcc.Dropdown(options=season_options,
                             value=2024,
                             id='season',
                             style={'backgroundColor': '#333333', 'color': '#FFFFFF'})
                    ], style={'backgroundColor': '#333333', 'color': '#FFFFFF', 'padding': '10px'})
                ], width=6),
                dbc.Col([
                    html.Label('Select Rounds:'),
                    html.Div([
                        dcc.Dropdown(['Round of 68', 'Round of 64', 'Round of 32', 'Sweet 16', 'Elite 8',
                            'Final 4', 'Final 2', 'Champion'], 'Round of 64',
                            multi=True,
                            id='rounds',
                            style={'backgroundColor': '#333333', 'color': '#FFFFFF'})
                    ], style={'backgroundColor': '#333333', 'color': '#FFFFFF', 'padding': '10px'})
                ], width=6),
                # html.Hr(style={'color': '#FFFFFF'})
                html.Br()
            ]),
            dbc.Row([
                html.Br(),
                dcc.Markdown('## Distribution of Beverage Sponsorship through March Madness',
                             style={'textAlign': 'center'}),
            ]),
            dbc.Row(id='graph-container')
        ])
    ]
)

@app.callback(
    Output(component_id='graph-container', component_property='children'),
    Input(component_id='season', component_property='value'),
    Input(component_id='rounds', component_property='value')
)
def update_graph(season, rounds_selected):
    template = 'plotly_dark'
    # Check if season is 2020
    if season == 2020:
        return [html.Div("No March Madness tournament was held in 2020 due to Covid-19 Restrictions.",
                         style={'fontSize': 24, 'textAlign': 'center'})]

    graphs = []
    round_order = ['Round of 68', 'Round of 64', 'Round of 32', 'Sweet 16', 'Elite 8',
                   'Final 4', 'Final 2', 'Champion']

    # Check if multiple rounds have been selected
    if isinstance(rounds_selected, list):
        rounds_selected_sorted = sorted(rounds_selected, key=lambda x: round_order.index(x))

        # Iterate over rounds
        for round in rounds_selected_sorted:
            # Create a filtered DataFrame for each selected round
            dff = df[(df['YEAR'] == season) & (df[round] > 0)]

            sponsor_counts = (dff['SPONSOR']
                              .value_counts()
                              .reset_index(name='Count')
                              .rename(columns={'SPONSOR': 'Sponsor'}))

            # Create a pie chart for the current round
            fig = px.pie(sponsor_counts,
                         values='Count',
                         names='Sponsor',
                         title=round,  # Set the title to a string
                         color='Sponsor',
                         color_discrete_map=custom_colors,
                         template=template)

            fig.update_layout(
                title={'text': round, 'font': {'size': 24}},  # Set the title
                legend={'font': {'size': 24}}
            ).update_traces(
                textinfo='percent+label',
                textfont_size=20
            )

            # Append the graph wrapped in a column
            graphs.append(dbc.Col(dcc.Graph(figure=fig), width=6))  # Adjust width as needed

        return graphs

    # If only one round is selected
    else:
        dff = df[(df['YEAR'] == season) & (df[rounds_selected] > 0)]

        sponsor_counts = (dff['SPONSOR']
                          .value_counts()
                          .reset_index(name='Count')
                          .rename(columns={'SPONSOR': 'Sponsor'}))

        fig = px.pie(sponsor_counts,
                     values='Count',
                     names='Sponsor',
                     title=rounds_selected,
                     color='Sponsor',
                     color_discrete_map=custom_colors,
                     template=template)

        fig.update_layout(
            title={
                'text': rounds_selected,  # Title text
                'font': {'size': 24}},  # Title font size,
            legend={
                'font': {'size': 24}  # Legend font size
            }
        ).update_traces(
            textinfo='percent+label',  # Display both percentage and label
            textfont_size=20  # Adjust the font size of the percentages and labels
        )
        return [dbc.Col(dcc.Graph(figure=fig), width=6)]  # Return a single graph wrapped in a column
if __name__ == '__main__':
    app.run(debug=True)