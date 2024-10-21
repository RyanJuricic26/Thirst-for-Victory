#!/usr/bin/env python
# coding: utf-8

# In[5]:

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from collections import defaultdict

# Creating file path for the data - maps from github
data_path = 'Data/Complete_Dataset.csv'

# Loading in data
data = pd.read_csv(data_path)

# Creating file path for the Boot-Strapped Distribution of Coke School's Mean Seed
bootstrap_dist_path = 'Data/Bootstrapped_Distribution.npy'

# Loading the distribution
bootstrap_means = np.load(bootstrap_dist_path)

def create_bootstrapped_distribution(df, num_reps):
    # Use pandas' sample method to generate all bootstraps at once
    # Reshape so each row is one bootstrap sample
    bootstrapped_samples = df['SEED'].sample(n=len(df) * num_reps, replace=True, random_state=42).values.reshape(
        num_reps, -1)

    # Calculate the mean of each bootstrap sample
    bootstrapped_means = np.mean(bootstrapped_samples, axis=1)

    return bootstrapped_means

def display_bootstrapped_distribution(dist, avg_pepsi_seed, conf_int=95):
    # FINISH
    excess = 100-conf_int
    left_value = 0 + (excess/2)
    right_value = 100 - (excess/2)
    left_interval_endpoint = np.percentile(dist, left_value)
    right_interval_endpoint = np.percentile(dist, right_value)
    interval = np.array([left_interval_endpoint, right_interval_endpoint])

    int_title = [round(interval[0], 2), round(interval[1], 2)]

    # Create the histogram for bootstrap_means using Plotly
    fig = go.Figure()

    # Add histogram
    fig.add_trace(go.Histogram(
        x=dist,
        nbinsx=50,  # Adjust the number of bins
        marker=dict(color='#fe001a'),
        name='Coke School\'s Boot-Strapped Mean Seed'
    ))

    # Add confidence interval (as a line or a bar)
    fig.add_trace(go.Scatter(
        x=interval,
        y=[0, 0],  # y-values are zero because it's a horizontal line
        mode='lines',
        line=dict(color='yellow', width=10),
        name=f'{conf_int}% Confidence Interval: {int_title}'
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
        title='Boot-Strapped Means of Coke School\'s Seed',
        xaxis_title='Seed',
        yaxis_title='Frequency',
        showlegend=True
    )

    # Update traces (set border color for histogram bars)
    fig.update_traces(
        marker=dict(
            line=dict(color='black', width=1)  # Set border color and width
        )
    )

    # Show the figure
    st.plotly_chart(fig)

def display_bev_pie_chart(season):

    page_title = f'{season} March Madness Beverage Distribution by Round: '
    st.markdown(f"<h3 style='text-align: center; color: white;'>{page_title}</h3>", unsafe_allow_html=True)
    # st.divider()

    # Displaying a message since 2020 did not have a march madness tournament
    if season == '2019-2020':
        st.subheader('Due to Covid Restrictions there was no March Madness tournament.')
        st.write('Please select another season to see more analytics.')

    else:
        # Splicing year from season
        year = int(season[-4:])

        # Creating a temporary dataframe of only that year
        temp_df = data[data['YEAR'] == year]

        # Creating a list of the rounds
        rounds = ['Round of 68', 'Round of 64', 'Round of 32', 'Sweet 16', 'Elite 8', 'Final 4', 'Final 2', 'Champion']

        # Setting colors for each sponsor
        custom_colors = {
            'Coke': '#F40000',  # Coke's main color
            'Pepsi': '#0E0E96',  # Pepsi's main color
            'Dr. Pepper': '#890024',  # Dr. Pepper's main color
            'BioSteel': '#00FF00',  # Green for BioSteel (no easily found color)
        }

        for round_name in rounds:

            # Filter for the current round
            round_df = temp_df[temp_df[round_name] > 0]

            # Count the number of occurrences for each sponsor
            sponsor_counts = round_df['SPONSOR'].value_counts().reset_index()
            sponsor_counts.columns = ['Sponsor', 'Count']  # Rename columns for clarity

            title = f'{round_name}'

            # Create the pie chart
            fig = px.pie(sponsor_counts, values='Count', names='Sponsor', title=title,
                         color='Sponsor', color_discrete_map=custom_colors)

            fig.update_layout(
                title={
                    'text': title,  # Title text
                    'font': {'size': 24},  # Title font size
                    #'x': 0.5,  # Center the title
                },
                legend={
                    'font': {'size': 24}  # Legend font size
                }
            )

            fig.update_traces(
                textinfo='percent+label',  # Display both percentage and label
                textfont_size=20  # Adjust the font size of the percentages and labels
            )

            # Show the plot
            st.plotly_chart(fig)

            st.divider()



def main():
    st.set_page_config(layout="wide")

    # Gives a title to the page
    st.markdown("<h1 style='text-align: center; color: #F40000;'>Thirst for Victory:</h1>", unsafe_allow_html=True)

    # Give a sub-title to the page
    st.markdown("<h3 style='text-align: center; color: white;'>An analysis of Beverage Sponsorship and it\'s effect on Team Performance.</h3>", unsafe_allow_html=True)

    # Custom CSS to make tabs bigger
    st.markdown("""
        <style>
        div[data-testid="stTabs"] button {
            font-size: 36px; /* Increase font size */
            padding: 10px 30px;   /* Increase padding for bigger tabs */
        }
        
        div[data-testid="stTabs"] button:hover {
            background-color: #0E0E96;
        }
        </style>
        """, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Overview of Project", "March Madness Distributions", "Analytics"])

    with tab1:
        st.markdown("<h1 style='text-align: center; color: White;'>Project Overview</h1>", unsafe_allow_html=True)
        st.subheader("Project Inception:")
        st.write("This project spawned from a small conversation between two professors who were arguing the relevance "
                 "of being a Coke/Pepsi D1 school. Dr. William Best had stated that his university, while still being "
                 "a D1 athletics school, was sponsored by Pepsi. This comment sparked the idea for this very project. "
                 "We began by formulating the idea of looking at the annual March Madness Tournament and seeing if "
                 "school's who were sponsored by Coca-Cola or Pepsico had an advantage.")

        st.subheader("Project Process:")
        st.write("To begin with, we needed to look at every school that has made the tournament in the since 2014. "
                 "This gave us 10 years of data to work with as due to Covid-19 restrictions there was no tournament "
                 "in 2020. From there we needed to know which beverage company that school had partnered with for the "
                 "season. Information on beverage sponsorship is sometimes tricky to find. Sometimes, schools are very "
                 "open about their partnerships and publish their contracts or write their own articles on the matter. "
                 "Other times, this information is a little harder to find. When we could not find a specific contract or "
                 "partnership annoucement, we had to dig deep. This quickly turned into watching home basketball games "
                 "for any given team on any given year and search for a couple of things. First, if a school used Gatorade "
                 "at home games they were classified as a Pepsi School. Likewise for Powerade being a Coke School. This is "
                 "because Coke owns Powerade and Pepsi owns Gatorade. If that was not obvious, we then resorted to looking "
                 "at advertisement displayed within their stadiums for that given year. If they advertised Coca-Cola and "
                 "there were no other public information to compare it against, a school was labeled as Coke. This was "
                 "repeated once again for every school in every year that they made the March Madness tournament. It was "
                 "also expanded on when contracts were made available to display any information we could find for subsequent "
                 "years. ")
    # Personal info fields
    with (tab2):

        # Adding a title to this tab
        st.markdown("<h1 style='text-align: center; color: White;'>Beverage Sponsor Distribution "
                    "Through March Madness</h1>", unsafe_allow_html=True)

        # Adding a subheader to select a season
        st.markdown("<h3 style='text-align: center; color: White;'>Select a season: </h3>", unsafe_allow_html=True)

        # I wanted to add tabs for each year to keep it very clean
        ssn2014, ssn2015, ssn2016, ssn2017, ssn2018, ssn2019, ssn2020, ssn2021, ssn2022, ssn2023, ssn2024 = st.tabs([
            "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021",
            "2021-2022", "2022-2023", "2023-2024"])

        with (ssn2014):
            season = "2013-2014"
            display_bev_pie_chart(season)

        with (ssn2015):
            season = "2014-2015"
            display_bev_pie_chart(season)

        with (ssn2016):
            season = "2015-2016"
            display_bev_pie_chart(season)

        with (ssn2017):
            season = "2016-2017"
            display_bev_pie_chart(season)

        with (ssn2018):
            season = "2017-2018"
            display_bev_pie_chart(season)

        with (ssn2019):
            season = "2018-2019"
            display_bev_pie_chart(season)

        with (ssn2020):
            season = "2019-2020"
            display_bev_pie_chart(season)

        with (ssn2021):
            season = "2020-2021"
            display_bev_pie_chart(season)

        with (ssn2022):
            season = "2021-2022"
            display_bev_pie_chart(season)

        with (ssn2023):
            season = "2022-2023"
            display_bev_pie_chart(season)

        with (ssn2024):
            season = "2023-2024"
            display_bev_pie_chart(season)

    with (tab3):
        # Creating the distribution of bootstrapped means
        coke_playoff_df = data[(data['SPONSOR'] == 'Coke') & (data['SEED'] > 0)]

        pepsi_playoff_df = data[(data['SPONSOR'] == 'Pepsi') & (data['SEED'] > 0)]
        avg_pepsi_seed = round(pepsi_playoff_df['SEED'].mean(), 2)

        # Adding a title to this tab
        st.markdown("<h1 style='text-align: center; color: White;'>Boot-Strapping Average Seed of Coke "
                    "Sponsored School\'s</h1>", unsafe_allow_html=True)

        # Adding a subheader to select a season
        st.markdown("<h3 style='text-align: center; color: White;'>Select a Confidence Interval: </h3>", unsafe_allow_html=True)

        conf90, conf95, conf97_5, conf99 = st.tabs(["90%", "95%", "97.5%", "99%"])

        with (conf90):
            conf_int = 90
            display_bootstrapped_distribution(dist=bootstrap_means, avg_pepsi_seed=avg_pepsi_seed, conf_int=conf_int)

        with (conf95):
            conf_int = 95
            display_bootstrapped_distribution(dist=bootstrap_means, avg_pepsi_seed=avg_pepsi_seed, conf_int=conf_int)

        with (conf97_5):
            conf_int = 97.5
            display_bootstrapped_distribution(dist=bootstrap_means, avg_pepsi_seed=avg_pepsi_seed, conf_int=conf_int)

        with (conf99):
            conf_int = 99
            display_bootstrapped_distribution(dist=bootstrap_means, avg_pepsi_seed=avg_pepsi_seed, conf_int=conf_int)


if __name__ == "__main__":
    main()