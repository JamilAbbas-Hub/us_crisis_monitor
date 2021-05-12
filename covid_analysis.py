#! /usr/bin/env python

# Author: Jamil Abbas
# Last Updated: 2021-05-07
#
#Script Description:
#This script takes in both US Crisis monitor data, and covid case data from the two states with the
#highest number of events based on the crisis monitor data (NY and CA). The script cleans up
#and creates a dataframe consisting of the number of events that occured per day, and the number
#of Covid-19 cases two weeks after that specific date. The range of dates observed are 2020-05-24 to 2020-09-15,
#as the majority of events occured in this time frame. A regression is done to see if there exists a relationship
#between the number of events that occured and the number of Covid-19 cases that are confirmed two weeks after. 

#####################
# REQUIRED MODULES  #
#####################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from create_spatial_visualization import clean_df

pd.options.mode.chained_assignment = None


#####################
# Global Variables  #
#####################
def create_clean_covid_df(fpath):
    '''
    This function takes in the covid data set for a specific state and returns a
    cleaned up dataframe of the data. A 'Date' column is created and populated
    with datetime objects of the case numbers, and the 'Cases(confirmed plus probable)'
    is transformed into an int object and the commas are removed.
    '''

    #Open the file and read in lines
    with open(fpath, 'r+') as f:
        content = f.readlines()

    content = [i.split() for i in content]
    content = content[1:]

    #Create a dataframe from the lines of the read in dataset
    df = pd.DataFrame(content[1:], columns=['Month',
                                        'Day',
                                        'Year',
                                        'Cases(confirmed plus probable)',
                                        'New cases',
                                        'Confirmed cases',
                                        'Probable Cases'])
    #Reverse the order of the dataframe so its chronological
    df = df.iloc[::-1]

    #Eliminiate commas from numbers in cases column
    df['Date'] = df['Month'].str.cat(df[['Day', 'Year']], sep=' ')
    df = df[['Date', 'Cases(confirmed plus probable)']]

    #Set date column as datetime object and set it as the index of the dataframe
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Cases(confirmed plus probable)'] = df['Cases(confirmed plus probable)'].str.replace(',','').astype(int)
    df.set_index('Date', inplace=True)

    return df


def combine_covid_protest_df(state, event_df, covid_df):
    '''
    This function combines the US Crisis monitor dataframes and the covid dataframe created in
    create_clean_covid_df. The covid cases are added on a two week lag to account for a delay in symptoms.
    For a specific date, the number of protests/other events that occured on that day is included,
    plus the number of covid cases two weeks after that specific date for means of comparison.
    '''

    #Chose only values from the selected state
    temp_df = event_df[event_df['state'] == state]
    temp_df['event_type'] = 'Protests'

    #Create dataframe based on the number of events per date
    main_df = pd.crosstab(temp_df['event_date'], temp_df['event_type'])

    idx = pd.date_range('2020-05-24', '2020-09-15')

    #Fill missing dates with 0 for 0 events
    main_df = main_df.reindex(idx, fill_value=0)

    #Take two week delay of covid cases and append to main df
    covid_list = covid_df['2020-06-07':'2020-09-29']['Cases(confirmed plus probable)'].tolist()
    main_df['2_week_delay_cases'] = covid_list

    return main_df

#########
# Main  #
#########
if __name__ == '__main__':

    event_df = clean_df(pd.read_csv('USA_2020_Nov14.csv'))

    #Create dataframe for california dataset
    cali_covid_df = create_clean_covid_df('cali_covid_data.txt')
    cali_main_df = combine_covid_protest_df('California', event_df, cali_covid_df)

    #Create dataframe for new york dataset
    ny_covid_df = create_clean_covid_df('ny_covid_data.txt')
    ny_main_df = combine_covid_protest_df('New York', event_df, ny_covid_df)

    #Perform regression on number of events in califorina and 2 week delayed covid Cases
    cali_X = cali_main_df['Protests']
    cali_Y = cali_main_df['2_week_delay_cases']

    cali_model = sm.OLS(cali_Y, cali_X)
    cali_results = cali_model.fit()
    print(cali_results.summary())

    #Perform regression on number of events in new york and 2 week delayed covid Cases
    ny_X = ny_main_df['Protests']
    ny_Y = ny_main_df['2_week_delay_cases']

    ny_model = sm.OLS(ny_Y, ny_X)
    ny_results = ny_model.fit()
    print(ny_results.summary())
