"""CSC110 Project: The Hidden Correlation Between Covid-19 and Hate Crimes in the United States

Module Description
==================
This module contains the data and functions to read hate_crime.csv file.
"""
from hate_crime import HateCrime
import hate_crime as hc
import plotly.graph_objects as go


###############################################################################
# Creating the graphs (month)
###############################################################################
def get_data_by_month(data: list[HateCrime], state: str) -> dict[tuple[int, int], int]:
    """Return a dictionary mapping (year, month) tuples to the corresponding number of hate crime
    incidences in the given state.

    Preconditions:
        - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',\
                    'IN', 'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT',\
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',\
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
    """
    hate_crime_data = {}

    for year in range(1999, 2021):
        for month in range(1, 13):
            hate_crime_data[(year, month)] = hc.num_instances_by_month(data, state, year, month)

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


def plot_hate_crime_by_month(data: list[HateCrime], state: str) -> None:
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
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',\
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
    """
    hate_crime_data = {}

    for year in range(1999, 2021):
        hate_crime_data[year] = hc.num_instances_by_year(data, state, year)

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


def plot_hate_crime_by_year(data: list[HateCrime], state: str) -> None:
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
