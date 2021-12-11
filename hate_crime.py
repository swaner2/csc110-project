"""CSC110 Project: The Hidden Correlation Between Covid-19 and Hate Crimes in the United States

Module Description
==================
This module contains the data and functions to read hate_crime.csv file.
"""
import csv
from dataclasses import dataclass
import datetime
from typing import List, Tuple
import plotly.graph_objects as go


@dataclass
class HateCrime:
    """"A data type representing a specific hate crime instance

    This corresponds to one row of tabular data found in hate_crime.csv

    Attributes:
        - incident_id: incident_id of the hate crime incident
        - state: abbreviated state name
        - date: date of the hate crime incident

    Representation invariants:
        - incident_id >= 0
        - 1999 <= date.year
        - len(state_abbr) == 2
        - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',\
                    'IN', 'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT',\
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OK', 'OR', 'PA', 'RI', 'SC',\
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}

    Even though there are many more headers, it is not needed in our project.
    """
    incident_id: int
    state_abbr: str
    date: datetime.date


def read_csv_file(filename: str) -> Tuple[List[str], List[HateCrime]]:
    """Return the headers and data stored in a csv file with the given filename.

        The return value is a tuple consisting of two elements:

        - The first is a list of strings for the headers of the csv file.
        - The second is a list of Delays (using the data class you just defined).

        Preconditions:
          - filename refers to a valid csv file with headers
    """
    with open(filename) as file:
        reader = csv.reader(file)
        row = next(reader)
        headers = [row[0], row[6], row[12]]
        data = [process_row(row) for row in reader]

    return (headers, data)


def process_row(row: List[str]) -> HateCrime:
    """Convert a row of hate crime incident data to HateCrime object.

    Preconditions:
        - row has the correct format for the hate crime data set.
    """
    return HateCrime(
        int(row[0]),
        row[6],
        str_to_date(row[12])
        )


def str_to_date(date_string: str) -> datetime.date:
    """Convert a string in yyyy-mm-dd format to a datetime.date

    Preconditions:
        - date_string has format yyyy-mm-dd

    >>> str_to_date('2011-01-05')
    datetime.date(2011, 1, 5)
    """
    date_string_split = str.split(date_string, '-')
    integer_date = [int(num) for num in date_string_split]

    return datetime.date(integer_date[0], integer_date[1], integer_date[2])


###############################################################################
# Operating on the data
###############################################################################
def num_instances_by_month(data: List[HateCrime], state: str, year: int, month: int) -> int:
    """Return the number of hate crime instances that occurred in the given state, month and year.

    Preconditions:
        - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',\
                    'IN', 'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT',\
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OK', 'OR', 'PA', 'RI', 'SC',\
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
        - 1999 <= year <= 2020
        - 1 <= month <= 12
    """
    num_of_instances = 0

    for row in data:
        if row.state_abbr == state and row.date.year == year and row.date.month == month:
            num_of_instances += 1

    return num_of_instances


def num_instances_by_year(data: List[HateCrime], state: str, year: int) -> int:
    """Return the number of hate crime instances that occurred in the given state and year.

    Preconditions:
        - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',\
                    'IN', 'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT',\
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OK', 'OR', 'PA', 'RI', 'SC',\
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
        - 1999 <= year <= 2020
    """
    num_of_instances = 0

    for row in data:
        if row.state_abbr == state and row.date.year == year:
            num_of_instances += 1

    return num_of_instances


def predictions(data: List[HateCrime]) -> dict[str, int]:
    """Takes hate crime data and returns a dictionary with the predicted number of hate crime
    incidents in 2020 per state"""
    states = {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
              'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
              'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
              'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}

    hate_crime_2020_predictions = {}

    for state in states:
        slope = find_best_slope(data, state, 1999, 2019)
        prediction = slope * num_instances_by_year(data, state, 2020) + \
            num_instances_by_year(data, state, 1999)
        hate_crime_2020_predictions[state] = prediction

    return hate_crime_2020_predictions


def find_best_slope(data: List[HateCrime], state: str, start_year: int, end_year: int) -> int:
    """Finds best slope of the hate crime trend to use for predicting the number of incidents"""
    start_incidents = num_instances_by_year(data, state, start_year)
    end_incidents = num_instances_by_year(data, state, end_year)

    slope = (end_incidents - start_incidents) // (end_year - start_year)

    middle_year = (end_year - start_year) // 2
    middle_incidents = num_instances_by_year(data, state, middle_year)

    adjusted_slope = (end_incidents - middle_incidents) // (end_year - middle_year)

    while abs(slope - adjusted_slope) > 1:
        slope = adjusted_slope

        middle_year = (end_year - middle_year) // 2
        middle_incidents = num_instances_by_year(data, state, middle_year)

        adjusted_slope = (end_incidents - middle_incidents) // (end_year - middle_year)

    return adjusted_slope


###############################################################################
# Creating the graphs (month)
###############################################################################
def get_data_by_month(data: list[HateCrime], state: str) -> dict[tuple[int, int], int]:
    """"Return a dictionary mapping (year, month) tuples to the corresponding number of hate crime
    incidences in the given state.

    Preconditions:
        - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',\
                    'IN', 'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT',\
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OK', 'OR', 'PA', 'RI', 'SC',\
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
    """
    hate_crime_data = {}

    for year in range(1999, 2021):
        for month in range(1, 13):
            hate_crime_data[(year, month)] = num_instances_by_month(data, state, year, month)

    return hate_crime_data


def get_xy_coordinates_month(data: list[HateCrime], state: str) -> tuple[list[str], list[int]]:
    """Return a tuple of two parallel lists. The first list the keys of the incidences as strings
    in the format 'year, month'. The second list contains the corresponding value of incidences.

    Preconditions:
        - incidences != {}
    """
    year_and_month = []
    value = []

    incidences = get_data_by_month(data, state)

    for row in incidences:
        year = str(row[0])
        month = str(row[1])
        year_and_month.append(year + ', ' + month)

        value.append(incidences[row])

    return (year_and_month, value)


def plot_hate_crime_data(data: list[HateCrime], state: str) -> None:
    """Plot hate crime data from a state as a time series.

    Preconditions:
        - incidences != {}
    """
    x_data, y_data = get_xy_coordinates_month(data, state)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name=state))

    fig.update_layout(title=f'Time Series of {state}',
                      xaxis_title='(Year, Month)',
                      yaxis_title=f'Calculated {state}')

    fig.show()


###############################################################################
# Creating the graphs (year)
###############################################################################
def get_data_by_year(data: list[HateCrime], state: str) -> dict[int, int]:
    """"Return a dictionary mapping (year, month) tuples to the corresponding number of hate crime
    incidences in the given state.

    Preconditions:
        - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',\
                    'IN', 'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT',\
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OK', 'OR', 'PA', 'RI', 'SC',\
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
    """
    hate_crime_data = {}

    for year in range(1999, 2021):
        hate_crime_data[year] = num_instances_by_year(data, state, year)

    return hate_crime_data


def get_xy_coordinates_year(data: list[HateCrime], state: str) -> tuple[list[str], list[int]]:
    """Return a tuple of two parallel lists. The first list the keys of the incidences as strings
    in the format 'year, month'. The second list contains the corresponding value of incidences.

    Preconditions:
        - incidences != {}
    """
    years = []
    value = []

    incidences = get_data_by_year(data, state)

    for row in incidences:
        year = str(row)
        years.append(year)

        value.append(incidences[row])

    return (years, value)


def plot_hate_crime_year(data: list[HateCrime], state: str) -> None:
    """Plot hate crime data from a state as a time series.

    Preconditions:
        - incidences != {}
    """
    x_data, y_data = get_xy_coordinates_year(data, state)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name=state))

    fig.update_layout(title=f'Time Series of {state}',
                      xaxis_title='(Year)',
                      yaxis_title=f'Calculated {state}')

    fig.show()


