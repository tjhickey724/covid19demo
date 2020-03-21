"""
  website_demo shows how to use templates to generate HTML
  from data selected/generated from user-supplied information
"""

from flask import Flask, render_template, request
from covid19 import get_covid_data
from time import time
app = Flask(__name__)

(all_data,us_data) = get_covid_data()
last_read = time()



@app.route('/',methods=['GET','POST'])
def covidlines():
	global all_data
	global last_read
	global us_data
	now = time()
	if now-last_read > 60*5: # read new data at most once every 5 minutes
		last_read=now
		(all_data,us_data) = get_covid_data()

	""" gets covid19 data """
	if request.method == 'GET':
		state='US'
		yaxistype='logarithmic'
	elif request.method == 'POST':
		state = request.form['state']
		yaxistype=request.form['yaxistype']

	if state=='US':
		data = us_data
		dataChecked = data[-1]['date']
	else:
		data = [x for x in all_data if x['state']==state]
		dateChecked = data[-1]['dateChecked']

	data.sort(key=lambda x: x['date'],reverse=False)
	positive = clean([d['positive'] for d in data])
	negative = clean([d['negative'] for d in data])
	pending = clean([d['pending'] for d in data])
	death = clean([d['death'] for d in data])
	total = clean([d['total'] for d in data])
	xs = [d['date'] for d in data]

	return render_template("covidlines.html",
	         state=state,
			 data=data,
			 xs=xs,
			 positive=positive,
			 negative=negative,
			 pending=pending,
			 death=death,
			 total=total,
			 yaxistype=yaxistype,
			 dateChecked=data[-1]['dateChecked'],
			 states = list(states.keys())
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
    app.run('0.0.0.0',port=3000)
