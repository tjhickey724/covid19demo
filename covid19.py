import json
import requests
def get_covid_data():
    """returns list of daily covid data for the state"""

    url = "https://covidtracking.com/api/states/daily"
    text = requests.get(url).text
    all_data = json.loads(text)
    #state_data = [x for x in all_data if x['state']==state]

    url = "https://covidtracking.com/api/us/daily"
    text = requests.get(url).text
    us_data = json.loads(text)
    for d in us_data:
        d['dateChecked'] = d['date']
    return (all_data,us_data)

def print_info(r):
    """
    r = {'date': 20200304,
         'state': 'MA',
         'positive': 2,
         'negative': None,
         'pending': None,
         'death': None,
         'total': 2,
         'dateChecked': '2020-03-04T21:00:00Z'}

    """
    print(r)

#recipes = get_recipes('stew',ingredients=['lamb','cabbage'])

if __name__ == '__main__':
    state = input("What state do you want to see?")
    (data,us) = get_covid_data()
    state_data = [d for d in data if d['state']==state]
    for r in state_data:
        print_info(r)
        print("\n*****************\n")
    print('bye!')
