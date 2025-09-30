import streamlit as st
import assignment2
import pandas as pd
import os
import time

st.write("# A2 Test Runner")

sample_ratio = st.number_input("## Sample Ratio",
                               value=None,
                               placeholder='Enter a Sample Ratio')

starting_date = st.date_input('Starting date')
ending_date = st.date_input('Ending date')

df = pd.read_csv('a2-countries.csv')
country_list = df['country'].to_list()

selected_countries = st.multiselect("Select Countries",
                                    country_list)



if st.button("Run", type='primary'):
    st.write("You selected:", list(selected_countries))

    start = time.time()
    country_csv = 'a2-countries.csv'
    assignment2.run(countries_csv_name=country_csv,
                    countries=selected_countries,
                    sample_ratio=sample_ratio,
                    start_date=starting_date,
                    end_date=ending_date)
    
    st.text("Running...")
    if os.path.exists('a2-covid-simulation.png'):
        st.image('a2-covid-simulation.png')

