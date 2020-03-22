import json
import requests
def get_world_covid_data():
    """returns list of daily covid data for the state"""

    url = "https://pomber.github.io/covid19/timeseries.json"
    text = requests.get(url).text
    all_data = json.loads(text)
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
                deaths += x['deaths']
                confirmed += x['confirmed']
                recovered += x['recovered']
    return {'date':d,
            'deaths':deaths,
            'confirmed':confirmed,
            'recovered':recovered}

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

#recipes = get_recipes('stew',ingredients=['lamb','cabbage'])

if __name__ == '__main__':
    country = input("What country do you want to see?")
    data = get_world_covid_data()
    cdata = data[country]
    for r in cdata:
        print_info(r)
        print("\n*****************\n")
    print('bye!')
