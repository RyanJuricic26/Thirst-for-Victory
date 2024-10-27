import dash
from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Project Overview')

layout = html.Div(
    [
        dbc.Row(
            [
                dcc.Markdown('## Project Overview',
                             style={'fontFamily': 'Old Standard TT'}),
                html.Br(),
                html.Br()
            ]
        ),
        dbc.Row(
            [
                dcc.Markdown('#### Project Inception:',
                             style={'fontFamily': 'Old Standard TT'})
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            This project spawned from a small conversation between two professors who were arguing the relevance
                            of being a Coke/Pepsi D1 school. Dr. William Best had stated that his university, while still being
                            a D1 athletics school, was sponsored by Pepsi. This comment sparked the idea for this very project.
                            We began by formulating the idea of looking at the annual March Madness Tournament and seeing if 
                            schools who were sponsored by Coca-Cola or Pepsico had an advantage.
                            """,
                            style={'textAlign': 'left',
                                   'fontSize': 18,
                                   'padding': '10px',
                                   'fontFamily': 'EB Garamond'}
                        )
                    ], width=10
                )
            ]
        ),
        dbc.Row(
            [
                dcc.Markdown('#### Data Collection Process:',
                             style={'fontFamily': 'Old Standard TT'})
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            To begin with, we needed to look at every school that has made the tournament since 2014.
                            This gave us 10 years of data to work with as, due to Covid-19 restrictions, there was no tournament
                            in 2020. From there, we needed to know which beverage company each school had partnered with for the
                            season. Information on beverage sponsorship is sometimes tricky to find. 
            
                            Sometimes, schools are very open about their partnerships and publish their contracts or write their
                            own articles on the matter. Other times, this information is a little harder to find. When we could 
                            not find a specific contract or partnership announcement, we had to dig deep. This quickly turned into
                            watching home basketball games for any given team in any given year to search for a couple of indicators.
            
                            First, if a school used Gatorade at home games, they were classified as a Pepsi school. Likewise, 
                            if they used Powerade, they were classified as a Coke school. This is because Coke owns Powerade and
                            Pepsi owns Gatorade. If that was not obvious, we then resorted to looking at advertisements displayed
                            within their stadiums for that given year. If they advertised Coca-Cola, and there was no other public
                            information to compare it against, a school was labeled as Coke.
            
                            This process was repeated for every school in every year that they made the March Madness tournament.
                            Whenever available, information on contracts was also added to display any relevant sponsorship details
                            for subsequent years.
                            """,
                            style={'textAlign': 'left',
                                   'fontSize': 18,
                                   'padding': '10px',
                                   'fontFamily': 'EB Garamond'}
                        )
                    ], width=10
                )
            ]
        )

    ]
)