import pandas as pd
import numpy as np
from sim_parameters import TRANSITION_PROBS, HOLDING_TIMES
from helper import create_plot


def create_sample_pop(countries_csv,countries,ratio):
    ## creating sample pop
    selected_countries = countries
    sample_ratio = ratio
    df = pd.read_csv(countries_csv)
    

    country_dets = df[df['country'].isin(selected_countries)]

    age_groups = list(TRANSITION_PROBS.keys())  # ['less_5', '5_to_14', '15_to_24','25_to_64', 'over_65']

    sample_pop = pd.DataFrame()
    sample_pop['country'] = country_dets['country']
    sample_pop['population'] = (country_dets['population']/sample_ratio).astype('int32')

    for group in age_groups:
        sample_pop[group] = round((df[group] * sample_pop['population'])/100)


    sample_pop.reset_index(drop=True, inplace=True)
    sample_pop.to_csv("Sample Population.csv")


    df = sample_pop.copy().drop('population',axis=1)
    # individual_person_dataframe['person_id'] = np.arange(total_sample_pop)

    df = df.melt(id_vars=['country'],
                value_vars=['less_5', '5_to_14', '15_to_24', '25_to_64','over_65'],
                var_name="age_group",
                value_name="pop").sort_values('country')

    df.reset_index(inplace=True,drop=True)
    df.to_csv("cap.csv")

def create_timeseries(starting_date, ending_date):
    start_date = starting_date
    end_date = ending_date
    df = pd.read_csv('cap.csv')
    date_range = pd.date_range(start=start_date, end=end_date)

    def next_state(age_group, state, staying_days, prev_state):
        if staying_days > 0:
            return state, staying_days-1, state
        
        states = list(TRANSITION_PROBS[age_group][state].keys())
        probs = list(TRANSITION_PROBS[age_group][state].values())

        new_state = np.random.choice(states, p=probs)
        staying_days = HOLDING_TIMES[age_group][new_state]

        return new_state, staying_days, prev_state
        
    rows = []
    i = 0
    for _, row in df.iterrows():
        for _ in range(int(row["pop"])):
            state, staying_days, prev_state = 'H', 0 ,'H'
            for d in date_range:        
                rows.append({
                    "person_id": i,
                    "country": row["country"],
                    "age_group": row["age_group"],
                    "date": d,
                    "state": state,
                    "staying_days" : staying_days,
                    "prev_state"   : prev_state,

                })
                state, staying_days, prev_state = next_state(age_group=row["age_group"],state=state, staying_days=staying_days, prev_state=prev_state)
            i += 1

    time_df = pd.DataFrame(rows)
    time_df.to_csv("a2-covid-simulated-timeseries.csv", index=False)


def summurize():
    df = pd.read_csv("a2-covid-simulated-timeseries.csv", parse_dates=['date'])

    df2 = df[['country', 'date','state']]
    df3 = df2.groupby(['date','country','state']).size().reset_index(name='count')

    df3 = df3.pivot_table(index=['date','country'], columns="state", values="count").fillna(0)
    df3.reset_index().to_csv("a2-covid-summary-timeseries.csv", index=False)


def plot(countries):
    print(countries)
    create_plot(summary_csv='a2-covid-summary-timeseries.csv', countries=countries)

def run(countries_csv_name,countries,sample_ratio,start_date,end_date):
    countries_csv = countries_csv_name
    create_sample_pop(countries_csv=countries_csv, countries=countries, ratio=sample_ratio)
    create_timeseries(starting_date=start_date,ending_date=end_date)
    summurize()
    plot(countries)


# SAMPLE_RATIO = 1e6
# countries=['Afghanistan','Sweden','Japan']
# # START_DATE = '2020-04-01'
# START_DATE = '2021-04-01'
# END_DATE = '2022-04-30'
# run(selected_countries=countries,
#     sample_ratio=SAMPLE_RATIO,
#     starting_date=START_DATE,
#     ending_date=END_DATE)