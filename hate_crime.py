"""CSC110 Project: The Hidden Correlation Between Covid-19 and Hate Crimes in the United States

Module Description
==================
This module contains the data and functions to read hate_crime.csv file.
"""
import csv
from dataclasses import dataclass
import datetime
from typing import List, Tuple

STATES = {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
          'IA', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
          'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
          'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}


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
                    'NB', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',\
                    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}

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
        rows = next(reader)
        headers = [rows[0], rows[6], rows[12]]
        data = [process_row(row) for row in reader]
        for instance in data:
            if instance.state_abbr == 'NB':
                instance.state_abbr = 'NE'

    return (headers, data)


def process_row(row: List[str]) -> HateCrime:
    """Convert a row of hate crime incident data to HateCrime object.

    Preconditions:
        - row has the correct format for the hate crime data set.
    """
    return HateCrime(
        int(row[0]),
        row[6],
        str_to_date(row[12]))


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
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',\
                    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
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
                    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',\
                    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WV', 'WI', 'WY'}
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

    hate_crime_2020_predictions = {}

    for state in STATES:
        slope = find_best_slope(data, state, 1999, 2019)
        prediction = slope + num_instances_by_year(data, state, 2019)
        if prediction < 1:
            prediction = 1
        hate_crime_2020_predictions[state] = prediction

    return hate_crime_2020_predictions


def find_best_slope(data: List[HateCrime], state: str, start_year: int, end_year: int) -> int:
    """Finds best slope of the hate crime trend to use for predicting the number of incidents"""
    start_incidents = num_instances_by_year(data, state, start_year)
    end_incidents = num_instances_by_year(data, state, end_year)

    slope = (end_incidents - start_incidents) // (end_year - start_year)

    middle_year = (end_year + start_year) // 2
    middle_incidents = num_instances_by_year(data, state, middle_year)

    adjusted_slope = (end_incidents - middle_incidents) // (end_year - middle_year)

    while abs(slope - adjusted_slope) > 1:
        slope = adjusted_slope

        middle_year = (end_year + middle_year) // 2
        middle_incidents = num_instances_by_year(data, state, middle_year)

        adjusted_slope = (end_incidents - middle_incidents) // (end_year - middle_year)

    return adjusted_slope


###############################################################################
# Calculating percent difference
###############################################################################
def instances_in_2020(data: List[HateCrime]) -> dict[str, int]:
    """Return a dictionary mapping the state to the corresponding number of hate crime instances
    in 2020."""
    hate_crime_instances_2020 = {}

    for state in STATES:
        hate_crime_instances_2020[state] = num_instances_by_year(data, state, 2020)

    return hate_crime_instances_2020


def calculate_percent_difference(data: List[HateCrime]) -> dict[str, list[float, int, int]]:
    """Return a dictionary mapping the abbreviated state name with the corresponding percent
    difference between the real and predicted hate crime instances in 2020.

    """
    percent_difference = {}

    predicted = predictions(data)
    actual = instances_in_2020(data)

    for state in STATES:
        percent_difference[state] = [(actual[state] - predicted[state]) / predicted[state] * 100,
                                     actual[state], predicted[state]]

    return percent_difference


def to_csv(percent_diff: dict[str, list[float, int, int]]) -> None:
    """Converts dictionary into csv file"""
    with open('percent_diff.csv', 'w', newline='') as pd_file:

        writer = csv.writer(pd_file)
        writer.writerow(['State', 'Percent Difference', 'Actual', 'Predicted'])
        for key, value in percent_diff.items():

            writer.writerow([key, value[0], value[1], value[2]])


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'csv', 'dataclasses', 'datetime',
                          'typing'],
        'allowed-io': ['read_csv_file', 'to_csv'],
        'disable': ['R1705']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
