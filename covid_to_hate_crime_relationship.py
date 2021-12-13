"""The Hidden Correlation Between Covid-19 and Hate Crimes in the United States
    From Jessica, Milena and Dian

Module Description
==================
This module contains functions to transform the data about covid cases and hate crime rates in the
United States into graphs.
"""
import plotly.graph_objects as go
from hate_crime import HateCrime, num_instances_by_month
from covid_dataclass import CovidData, processing_data


def get_xy_data(covid_data: list[CovidData], hate_crime_data: list[HateCrime], state: 'str') -> \
        tuple[list[str], list[int], list[int]]:
    """Return a tuple of 3 parallel lists.
    The first list contains strings in the format 'month, year'.
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
            list.append(hate_crimes, num_instances_by_month(hate_crime_data, state, 2020,
                                                            x.date.month))
    return dates, covid_nums, hate_crimes


def plot_covid_and_hate_crime(covid_data: list[CovidData], hate_crime_data: list[HateCrime],
                              state: 'str') -> None:
    """Plot the relationship between covid rates and hate crime rates for a given state.
    Each point represents a different month in 2020.
    Preconditions:
        - state in {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', \
                         'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', \
                         'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', \
                         'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', \
                         'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}
    """

    _, x_data, y_data = get_xy_data(covid_data, hate_crime_data, state)

    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, mode='markers'))

    fig.update_layout(title=f'The Correlation Between Covid Rates and Hate Crime in {state}',
                      xaxis_title='Covid Rate',
                      yaxis_title='Hate Crime Rate')

    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'plotly.graph_objects', 'hate_crime',
                          'covid_dataclass'],
        'disable': ['R1705']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
