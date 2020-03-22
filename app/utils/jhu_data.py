from collections import defaultdict
from csv import DictReader
from datetime import datetime, timedelta

import requests
from cachetools import cached, TTLCache


JHU_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{day}.csv'


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_country_data(days_back=1):
    """
    Gets data by country from daily CSV from JHU COVID-19 data Github repository
    for a given day

    Parameters
    ----------
    days_back: int
        Number of days from today to look back

    Returns
    -------
    dict[dict]:
        JHU totals by country
            {
                'country' : str :
                {
                    'confirmed' : int,
                    'deaths' : int,
                    'recovered' : int
                }
            }
    """
    country_totals = defaultdict(dict)
    day = (datetime.today() - timedelta(days_back)).strftime('%m-%d-%Y')
    request = requests.get(JHU_URL.format(day=day))

    data = DictReader(request.text.splitlines())
    for row in data:
        country = row.get('Country/Region', '')
        confirmed = int(row.get('Confirmed', 0))
        deaths = int(row.get('Deaths', 0))
        recovered = int(row.get('Recovered', 0))
        last_updated = row.get('Last Update', '')

        if country not in country_totals:
            country_totals[country]['confirmed'] = confirmed
            country_totals[country]['deaths'] = deaths
            country_totals[country]['recovered'] = recovered
            country_totals[country]['last_updated'] = last_updated
        else:
            country_totals[country]['confirmed'] += confirmed
            country_totals[country]['deaths'] += deaths
            country_totals[country]['recovered'] += recovered
    return country_totals

def get_global_cases(days_back=1):
    """
    Gets global number of cases from JHU data

    Parameters
    ----------
    days_back: int
        Number of days from today to look back

    Returns
    -------
    dict:
        {
            'confirmed' : int,
            'deaths' : int,
            'recovered' : int
        }
    """
    global_cases = {}
    data = get_country_data()
    global_cases['confirmed'] = sum(c['confirmed'] for c in data.values() if c)
    global_cases['deaths'] = sum(c['deaths'] for c in data.values() if c)
    global_cases['recovered'] = sum(c['recovered'] for c in data.values() if c)
    return global_cases
