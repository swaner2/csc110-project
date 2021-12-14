"""CSC110 Project: The Hidden Correlation Between Covid-19 and Hate Crimes in the United States

Main Module

Module Description
==================
This module contains the important key functions and dataclasses of the project.
"""
from hate_crime import read_csv_file, calculate_percent_difference, to_csv
from covid_dataclass import read_csv_file as read_csv_file_covid
from map import make_map
from creating_graphs import plot_hate_crime_by_year, plot_hate_crime_by_month
from covid_to_hate_crime_relationship import plot_covid_and_hate_crime

hate_crime_data = read_csv_file('hate_crime.csv')[1]
covid_data = read_csv_file_covid('all-states-history.csv')


def run() -> None:
    """This function creates the map which visualizes the relationship between hate crime rates
    and covid case rates.
    """
    percent_diff = calculate_percent_difference(hate_crime_data)
    to_csv(percent_diff)
    make_map()


def graphs() -> None:
    """This function creates 3 graphs of each type for a state.
    Type 1: the trend of hate crime from 1999-2020
    Type 2: the trend of hate crime by month
    Type 3: the correlation between covid rates and hate crime rates
    The default state is set to Alabama, which is an example of a state whose
    hate crime rate was drastically higher than predicted in 2020.
    """
    plot_hate_crime_by_year(hate_crime_data, 'AL')
    plot_hate_crime_by_month(hate_crime_data, 'AL')
    plot_covid_and_hate_crime(covid_data, hate_crime_data, 'AL')
    # to create the graphs for a different state, replace 'AL' with the string \
    # of the abbreviation of the state you would like to look at. For example, \
    # Maryland is another state with interesting trends. To see its graphs, replace 'AL' with 'MD'.
