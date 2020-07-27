import json
import requests

"""
This module gets the lastest daily covid 19 data elements from pomber.github.io/covid18
which in turn gets its data from John Hopkins University

  https://github.com/CSSEGISandData/COVID-19

This module also defines the getCountryPop(c) function which returns the 2019 population 
of the country c.  It uses the same names as in the John Hopkins University dataset
"""

def get_world_covid_data():
    """returns list of daily covid data for the state"""

    url = "https://pomber.github.io/covid19/timeseries.json"
    text = requests.get(url).text
    all_data = json.loads(text)
    #print(all_data)
    world_data = summarize(all_data)
    return (all_data,world_data)

def summarize(data):
    """ create a summary of world stats for all days"""
    dates = [d['date'] for d in data['US']]
    result = []
    for d in dates:
        result += [summarize_date(d,data)]
    return result

def summarize_date(d,data):
    """ create a summary of the
         confirmed, deaths, recovered
         for the data and all countries
    """
    deaths=0
    confirmed=0
    recovered=0
    for c in data:
        for x in data[c]:
            if x['date']==d:
                deaths += clean(x['deaths'])
                confirmed += clean(x['confirmed'])
                recovered += clean(x['recovered'])
    return {'date':d,
            'deaths':deaths,
            'confirmed':confirmed,
            'recovered':recovered}

def averageList(k,L):
    """ average data over k days"""
    week = [0]*k
    newL=[]
    for x in L:
        week = week[1:]+[x]
        newL += [sum(week)/k]
    return newL

def clean(x):
	if type(x)==int:
		return x
	else:
		return 0

def collect(key,d,data):
    return [[t[key] for t in data[c]] for c in data.keys()]


def print_info(r):
    """
    r =
        {
          "date": "2020-1-22",
          "confirmed": 2,
          "deaths": 0,
          "recovered": 0
        },

    """
    print(r)

countryData = json.load(open("data/country-by-population.json","r"))

countryNames = {
'Cabo Verde':'Cape Verde'
,'Congo (Brazzaville)':'Congo'
,'Congo (Kinshasa)':'The Democratic Republic of Congo'
,"Cote d'Ivoire":'Ivory Coast'
,"Diamond Princess":'none'
,"Czechia":'Czech Republic'
,"Eswatini":'Swaziland'
,"Fiji":'Fiji Islands'
,"Holy See":'Holy See (Vatican City State)'
,"Korea, South":'South Korea'
,"Russia":'Russian Federation'
,"Serbia":"Serbia"
,"Sri Lanka":"SriLanka"
,"Taiwan*":'none'
,"US":'United States'
,"Timor-Leste":'East Timor'
,"Libya":'Libyan Arab Jamahiriya'
,"West Bank and Gaza":'none'
,"Kosovo":'none'
,"Burma":'Myanmar'
,"MS Zaandam":'none'
}

def getCountryPop(country):
    cname=country
    if country in countryNames:
        cname = countryNames[country]
    if cname=='none':
        pop=0
    else:
        pop = countryPop(cname)
    if pop==0:
        print("country with no population ",country)
        return(1000000000000)
    else:
        return(pop)

def countryPop(country):
    cs = [d['population'] for d in countryData if d['country']==country]
    return cs[0] if len(cs)==1 else 0


#recipes = get_recipes('stew',ingredients=['lamb','cabbage'])

if __name__ == '__main__':
    country = input("What country do you want to see?")
    data = get_world_covid_data()
    cdata = data[country]
    for r in cdata:
        print_info(r)
        print("\n*****************\n")
    print('bye!')
