"""The Hidden Correlation Between Covid-19 and Hate Crimes in the United States
    From Jessica, Milena and Dian

Module Description
==================
This module contains functions to transform the data about covid cases and hate crime rates in the United States
into graphs.

"""
import csv
import plotly.graph_objects as go
from hate_crime import HateCrime
from covid_dataclass import CovidData
from dataclasses import dataclass
import datetime
from typing import List, Tuple


###############################################################################
# Hate Crime Functions
###############################################################################
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
# Operating on the hate crime data
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


###############################################################################
# Covid Rate Functions
###############################################################################

@dataclass
class CovidData:
    """The level of covid cases in a certain time of a certain state.

    Instance Attributes:
       - date: the day on which the covid cases were reported
       - state: the US state the data relates to
       - cases: the number of positive covid cases reported in the state on that day

    Representation Invariants:
        - (2021, 1, 1) > self.date >= (2020, 1, 1)
        - self.state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', \
                         'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', \
                         'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', \
                         'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', \
                         'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}
        - self.cases >= 0

    """
    date: datetime.date
    state: str
    cases: int


def read_csv_file2(filename: str) -> list[CovidData]:
    """Process and return the relevant data stored in a csv file with the given filename.

    The return value is a list of the data in the file in the form of the dataclass defined above.

    Preconditions:
      - filename refers to a valid csv file with headers

    """
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        data = []
        for row in reader:
            processed_row = process_row2(row)
            if processed_row.date.year == 2020:
                data.append(processed_row)
    return data


def process_row2(row: list[str]) -> CovidData:
    """Convert a row of covid case data to a CovidCase dataclass.

    """
    (year, month, day) = str.split(row[0], '-')
    date = datetime.date(int(year), int(month), int(day))
    state = row[1]
    if row[21] == '':
        cases = 0
    else:
        cases = int(row[21])
    return CovidData(date, state, cases)


def cases_by_month(covid_data: list[CovidData], month: int, state: str) -> CovidData:
    """Take the dataclasses from the file and combine the cases from for each day to per month.

    The whole month's total covid cases will be represented by the case count on the first day of the month.

    """
    date = datetime.date(2020, month, 1)
    total_cases = 0
    for row in covid_data:
        if row.date.month == month and row.state == state:
            total_cases = total_cases + row.cases
    return CovidData(date, state, total_cases)


def processing_data(raw_covid_data: list[CovidData]) -> list[CovidData]:
    """Take the data read from the file and compile it for monthly totals for each state."""

    data_by_month = []
    for state in ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                  'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                  'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                  'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']:
        for x in range(1, 13):
            month_total = cases_by_month(raw_covid_data, x, state)
            list.append(data_by_month, month_total)
    return data_by_month


###############################################################################
# Functions to Plot it
###############################################################################

def get_xy_data(covid_data: list[CovidData], hate_crime_data: list[HateCrime], state: 'str') -> \
        tuple[list[str], list[int], list[int]]:
    """Return a tuple of 3 parallel lists. The first list contains strings in the format 'month, year'.
    The second list contains the corresponding number of new covid cases.
    The third list contains the corresponding number of hate crimes.

    Preconditions:
    - len(covid_data) > 0
    - len(covid_data) = len(hate_crime_data)
    - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', \
                         'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', \
                         'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', \
                         'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', \
                         'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}
    """
    dates = []
    covid_nums = []
    hate_crimes = []
    covid_data_by_month = processing_data(covid_data)
    for x in covid_data_by_month:
        if x.state == state:
            date = (x.date.month, 2020)
            list.append(dates, date)
            list.append(covid_nums, x.cases)
            list.append(hate_crimes, num_instances_by_month(hate_crime_data, state, 2020, x.date.month))
    return dates, covid_nums, hate_crimes


def plot_covid_and_hate_crime(covid_data: list[CovidData], hate_crime_data: list[HateCrime], state: 'str') -> None:
    """Plot the relationship between covid rates and hate crime rates for a given state.
    Each point represents a different month in 2020.

    Preconditions:
        - add?!
    """
    # Convert the outputs into parallel x and y lists
    _, x_data, y_data = get_xy_data(covid_data, hate_crime_data, state)

    # Create the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name=state))

    # Configure the figure
    fig.update_layout(title=f'The Correlation Between Covid Rates and Hate Crime in {state}',
                      xaxis_title='Covid Rate',
                      yaxis_title=f'Hate Crime Rate')

    # Show the figure in the browser
    fig.show()
    # Is the above not working for you? Comment it out, and uncomment the following:
    # fig.write_html('my_figure.html')
    # You will need to manually open the my_figure.html file created above.
