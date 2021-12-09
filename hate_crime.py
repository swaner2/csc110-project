"""CSC110 Project: The Hidden Correlation Between Covid-19 and Hate Crimes in the United States

Module Description
==================
This module contains the data and functions to read hate_crime.csv file.
"""
import csv
from dataclasses import dataclass
import datetime
from typing import List, Tuple


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

    Even though there are many more headers, it is not needed due to the
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
