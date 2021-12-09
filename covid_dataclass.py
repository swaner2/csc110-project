"""The Hidden Correlation Between Covid-19 and Hate Crimes in the United States
    From Jessica, Milena and Dian

Module Description
==================
This module contains covid to transform the raw data about covid cases in the United States into workable dataclasses.

"""
import csv
from dataclasses import dataclass
import datetime


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


def read_csv_file(filename: str) -> list[CovidData]:
    """Process and return the relevant data stored in a csv file with the given filename.

    The return value is a list of the data in the file in the form of the dataclass defined above.

    Preconditions:
      - filename refers to a valid csv file with headers

    """
    with open(filename) as file:
        reader = csv.reader(file)
        headers = next(reader)    # idk how to not count the first row
        data = []
        for row in reader:
            processed_row = process_row(row)
            if processed_row.date.year == 2020:
                data.append(processed_row)
    return data


def process_row(row: list[str]) -> CovidData:
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
            total_cases += 1
    return CovidData(date, state, total_cases)


def processing_data(raw_covid_data: list[CovidData]) -> list[CovidData]:
    """Take the data read from the file and compile it for monthly totals for each state."""

    data_by_month = []
    for state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                  'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                  'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                  'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}:
        for x in range(1, 13):
            month_total = cases_by_month(raw_covid_data, x, state)
            list.append(data_by_month, month_total)
    return data_by_month

