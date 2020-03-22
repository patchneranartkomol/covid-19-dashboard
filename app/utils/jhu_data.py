import csv
from collections import defaultdict
from datetime import datetime, timedelta

import requests
from cachetools import cached, TTLCache


YESTERDAY = (datetime.today() - timedelta(1)).strftime('%m-%d-%Y')
JHU_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{day}.csv'


def get_country_data(day=YESTERDAY):
	"""
	Gets data by country from daily CSV from JHU COVID-19 data Github repository

	Parameters
	----------
	day: str 
		Formatted date to retrieve the corresponding CSV

	Returns
	-------
	dict[dict]:
		JHU totals by country
			{
				'Country' : str,
				'Confirmed' : int,
				'Deaths' : int,
				'Recovered' : int
			}
	"""
	country_totals = defaultdict(dict)
	request = requests.get(JHU_URL.format(day=day))

	data = csv.DictReader(request.text.splitlines())
	for row in data:
		country = row.get('Country/Region', '')
		confirmed = int(row.get('Confirmed', 0))
		deaths = int(row.get('Deaths', 0))
		recovered = int(row.get('Recovered', 0))

		if country not in country_totals:
			country_totals[country]['Confirmed'] = confirmed
			country_totals[country]['Deaths'] = deaths
			country_totals[country]['Recovered'] = recovered
		else:
			country_totals[country]['Confirmed'] += confirmed
			country_totals[country]['Deaths'] += deaths
			country_totals[country]['Recovered'] += recovered
	return country_totals

print(get_country_data())
