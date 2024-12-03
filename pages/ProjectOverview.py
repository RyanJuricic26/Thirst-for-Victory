import dash
from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Project Overview')

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
            
                            This process was repeated for every school, in every year that they made the March Madness tournament.
                            Whenever available, information on contracts was also added to display any relevant sponsorship details
                            for subsequent years. Such as if a university published their 10 year contract with Pepsi from 2012-2022, 
                            that was recorded for all subsequent years regardless if they made the tournament in all years. 
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
                dcc.Markdown('#### Project Findings:',
                             style={'fontFamily': 'Old Standard TT'})
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            This project was initialy completed using only the data from 2024. We wanted to see if there was 
                            any association in beverage sponsor and how far a team went in the March Madness Tournament. Our 
                            hypothesis was that there was no significant association and that beverage sponsor was an independent 
                            variable. The alternate hypothesis was that there was a significant association between the two. 

                            In order to test our hypothesis, we chose to do a Fisher's Exact Test. We chose this due to our very small 
                            sample size of only 64 teams (For our initial project we did not include the round of 68). We set our 
                            significance level to 95%. This means a p-value under 0.05 would lead us to reject our null hypothesis 
                            that there is not a significant association between beverage sponsor and final standings in the March 
                            Madness Tournament. 

                            Upon running our test over the number of Pepsi and Coke schools in each round for the 2024 March Madness 
                            Tournament, we calculated a p-value of 0.00282. Since our significance level was set to 95%, our p-value 
                            is well within the threshold to reject our null hypothesis. 

                            This was our R Code that was ran to perform our Fisher's Exact Test:

                            library(tidyverse)
                            # 2024

                            # Coke Data
                            coke <- tibble(
                            "Sponsor" = c(rep("Coke", 63)),
                            "Round" = c(rep("R64", 28), rep("R32", 11), rep("N16", 11), rep('N8', 7), rep("N4", 4), rep("N2", 2))
                            )

                            # Pepsi Data
                            pepsi <- tibble(
                            "Sponsor" = c(rep("Pepsi", 63)),
                            "Round" = c(rep("R64", 36), rep("R32", 21), rep("N16", 5), rep("N8", 1))
                            )

                            # Combine
                            total <- bind_rows(coke, pepsi)

                            # Perform Fisher's exact test
                            fisher_result <- fisher.test(table(total$Sponsor, total$Round))

                            # Print the result
                            print(fisher_result)

                            Check out the March Madness Tab in order to see the results from 2024's tournament to see how beverage 
                            sponsorship was distributed through each round!
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