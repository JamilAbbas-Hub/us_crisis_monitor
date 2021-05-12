#####################
# REQUIRED MODULES  #
#####################
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime

#####################
# Global Variables  #
#####################

def clean_df(dataframe):

    '''
    Name: clean_df
    Inputs: df, pandas dataframe of the ACLED US Crisis Monitor data
    Objective: Takes in the original US Crisis Monitor data as a dataframe and cleans the data.
    This includes transforming the 'EVENT_DATE' column into a datetime object,
    eliminiating unneeded columns,
    renaming columns,
    setting column names to lowercase,
    creating a 'month' column that extracts the month of the event as an integer.
    '''

    pd.options.mode.chained_assignment = None
    #Transform 'EVENT_DATE' to datetime object
    dataframe['EVENT_DATE'] = pd.to_datetime(dataframe['EVENT_DATE'], format='%d-%B-%Y')

    #Select important columns
    dataframe = dataframe[['EVENT_DATE', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', 'ADMIN1','ADMIN2',
            'LATITUDE', 'LONGITUDE', 'FATALITIES']]

    #Rename columns and make them lowercase
    dataframe.rename(columns = {'ADMIN1': 'state', 'ADMIN2':'city'}, inplace=True)
    dataframe.columns = [name.lower() for name in dataframe.columns]

    #Extract month from event_date into seperate column
    dataframe['month'] = pd.DatetimeIndex(dataframe['event_date']).month

    print('----- Dataframe Successfully Cleaned -----')
    return dataframe






def create_visual(dataframe, by_month=False):

    '''
    Name: create_visual
    Inputs: df, cleaned pandas dataframe (from clean_df function)
            by_month, boolean to determine whether or not to create the visual by month value or not
    Objective: Take in the cleaned dataframe from clean_df and create a plotly visualization of the data.
    User decides whether to visualize by month or not. If by_month is set to False, then the
    visualiztion will be created by 'event_type'.
    '''

    months = {5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November'}
    colors = [ 'lightseagreen', 'orange', 'chocolate', 'purple', 'crimson', 'salmon',  'cyan']

    #Array of the different event types
    event_types = dataframe.event_type.value_counts().index.array

    fig = go.Figure()

    if by_month:
        #curr = {5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November'}
        curr = [5,6,7,8,9,10,11]
        names = ['May', 'June', 'July', 'August', 'September', 'October', 'November']
        label = 'month'
        text_label = 'event_type'
        title = '2020 United States Political Violence/Demonstrations by Month'
        fname = './visuals/geo_visual_by_month.html'
    else:
        curr = dataframe.event_type.value_counts().index.array
        names = curr
        label = 'event_type'
        text_label = 'city'
        title = 'Total United States Political Violence/Demonstrations  (5/24/2020 - 11/14/2020)'
        fname = './visuals/geo_visual_event_type.html'

    for i in range(len(curr)):
        temp_df = dataframe[dataframe[label] == curr[i]]
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=temp_df['longitude'],
            lat=temp_df['latitude'],
            text=temp_df[['city']],
            name=names[i],
            mode='markers',
            marker=dict(
                line_width=0.5,
                color = colors[i],
                sizeref=9,
                sizemode='area',
                reversescale=True)))

    fig.update_geos(fitbounds='locations',
               resolution=110,
               landcolor='rgb(217, 217, 217)',
               scope='usa',
               showcountries=True, countrycolor='Black',
               showsubunits=True, subunitcolor='White')
    fig.update_layout(title_text=title, title_x=0.5)
    plotly.offline.plot(fig, filename=fname)

    print('----- Visualization Successfully Created -----')



#########
# Main  #
#########
if __name__ == '__main__':


    #Import/clean the Dataframe
    df = clean_df(pd.read_csv('USA_2020_Nov14.csv'))

    #Create visual by event_type
    create_visual(df, by_month=False)

    #Create visual by month
    create_visual(df, by_month=True)
