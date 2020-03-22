"""
  website_demo shows how to use templates to generate HTML
  from data selected/generated from user-supplied information
"""

from flask import Flask, render_template, request
from covid19 import get_covid_data
from covid19world import get_world_covid_data

from time import time

def fix_country(c):
	return c.replace(' ','_').replace(',','_')


app = Flask(__name__)

(states_data,us_data) = get_covid_data()

last_read = time()
last_world_read = time()

(countries_data,world_data) = get_world_covid_data()

countries_data = {fix_country(c):countries_data[c] for c in countries_data.keys()}
countries = list(countries_data.keys())
countries.sort()
countries_data['world']=world_data
#countries = [c.replace(', ','_') for c in countries] # for 'Korea, South'
print('countries')
print(countries)



@app.route('/')
def main():
	return render_template('covid_data.html')

@app.route('/us',methods=['GET','POST'])
def covidlines():
	global states_data
	global last_read
	global us_data
	now = time()
	if now-last_read > 60*60: # read new data at most once every 60 minutes
		last_read=now
		(states_data,us_data) = get_covid_data()
		print('updated states covid data',now)


	""" gets covid19 data """
	if request.method == 'GET':
		state='MA'
		yaxistype='logarithmic'
	elif request.method == 'POST':
		state = request.form['state']
		yaxistype=request.form['yaxistype']

	if state=='US':
		data = us_data
		dataChecked = data[-1]['date']
	else:
		data = [x for x in states_data if x['state']==state]
		dateChecked = data[-1]['dateChecked']

	data.sort(key=lambda x: x['date'],reverse=False)
	positive = clean([d['positive'] for d in data])
	negative = clean([d['negative'] for d in data])
	pending = clean([d['pending'] for d in data])
	hospitalized = clean([d['hospitalized'] for d in data])
	death = clean([d['death'] for d in data])
	total = clean([d['total'] for d in data])
	xs = [d['date'] for d in data]

	return render_template("statecovidlines.html",
	         state=state,
			 data=data,
			 xs=xs,
			 positive=positive,
			 negative=negative,
			 pending=pending,
			 hospitalized=hospitalized,
			 death=death,
			 total=total,
			 yaxistype=yaxistype,
			 dateChecked=data[-1]['dateChecked'],
			 states = list(states.keys())
			 )

@app.route('/about')
def about():
  return render_template("about.html")


@app.route('/world',methods=['GET','POST'])
def world():
	global countries_data
	global last_world_read
	global countries
	now = time()
	if now-last_world_read > 60*60: # read new data at most once every 60 minutes
		last_world_read=now
		(countries_data,world_data) = get_world_covid_data()
		countries_data = {fix_country(c):countries_data[c] for c in countries_data.keys()}
		countries = list(countries_data.keys())
		countries.sort()
		countries_data['world']=world_data
		print('updated world_covid_data',now)
		#countries = [c.replace(', ','_') for c in countries] # for 'Korea, South'


	if request.method == 'GET':
		country='world'
		yaxistype='logarithmic'
	elif request.method == 'POST':
		country = request.form['country']
		yaxistype=request.form['yaxistype']

	data = countries_data[country]
	print('country',country)

	confirmed = clean([d['confirmed'] for d in data])
	deaths = clean([d['deaths'] for d in data])
	recovered = clean([d['recovered'] for d in data])


	xs = [d['date'] for d in data]


	return render_template("worldcovidlines.html",
	         country=country,
			 data=data,
			 xs=xs,
			 confirmed=confirmed,
			 deaths=deaths,
			 recovered=recovered,
			 yaxistype=yaxistype,
			 countries=countries
			 )



def clean(data):
	return [f(d) for d in data]

def f(x):
	if type(x)==int:
		return x
	else:
		return 0

states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

print('states=')
print(list(states.keys()))

if __name__ == '__main__':
    #app.run('0.0.0.0',port=4000)
	app.run('turing.cs-i.brandeis.edu',port=4000)
