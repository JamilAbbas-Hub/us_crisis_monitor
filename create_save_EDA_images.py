#! /usr/bin/env python

# Author: Jamil Abbas
# Last Updated: 2021-05-07
#
#Script Description:
#This script takes in the US Crisis Monitor dataset and creates a series of visualizations
#for the purpose of creating an exploratory data analysis. The visualizations include:
#Type of demonstrations by proportion
#Top 10 states with the most events
#Top 15 cities with the most events
#Proportion of events by month of occurance

#####################
# REQUIRED MODULES  #
#####################
from create_spatial_visualization import clean_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#####################
# Global Variables  #
#####################

'''
Each of the following functions takes in the cleaned dataframe and creates a specific
visualization and then saves the file to the 'visuals/EDA Images'.
'''


    #Type of demonstrations by proportion
def plot_type_demonstrations(df):
    labels = ['Protests', 'Other']
    count = [df.event_type.value_counts()['Protests'], sum(df.event_type.value_counts()[1:])]

    plt.figure(figsize=(16,9))
    plt.title('Types of Demonstrations')
    plt.pie(count, labels=labels, shadow=False, autopct='%1.1f%%', startangle=90)
    plt.savefig('./visuals/EDA Images/type_demonstrations.png')
    print('-----Image Successfully Created-----')

    #Top 10 states with the most events
def plot_top_state_events(df):

    state = df.state.value_counts()[:10]

    plt.figure(figsize=(16,9))
    plt.bar(state.index, state, color='purple')
    plt.title('Top 10 States with Highest Event Count', fontsize=18)

    for i in range(len(state)):
        plt.annotate(str(state[i]), xy=(i, state[i]), ha='center', va='bottom')

    plt.savefig('./visuals/EDA Images/top_state_events.png')
    print('-----Image Successfully Created-----')

    #Top 15 cities with the most events
def plot_top_city_events(df):

    city = df.city.value_counts()[:15]

    plt.figure(figsize=(16,9))
    plt.bar(city.index, city, color='green')
    plt.xticks(rotation=-45)
    plt.title('Top 15 Cities with Highest Event Count', fontsize=18)

    for i in range(len(city)):
        plt.annotate(str(city[i]), xy=(i, city[i]), ha='center', va='bottom')

    plt.savefig('./visuals/EDA Images/top_city_events.png')
    print('-----Image Successfully Created-----')

    #Proportion of events by month of occurance
def plot_proportion_month(df):

    month = df.month.value_counts()
    labels = ['June', 'August', 'July', 'September', 'October', 'May', 'November']

    plt.figure(figsize=(20,11))
    plt.pie(month[:], labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Proportion of Events by Month', fontsize=17)
    plt.savefig('./visuals/EDA Images/proportion_by_month.png')
    print('-----Image Successfully Created-----')





#########
# Main  #
#########
if __name__ == '__main__':

    df = clean_df(pd.read_csv('USA_2020_Nov14.csv'))

    plot_type_demonstrations(df)

    plot_top_state_events(df)

    plot_top_city_events(df)

    plot_proportion_month(df)
