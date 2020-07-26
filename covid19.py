import json
import requests
import matplotlib.pyplot as plt
import numpy as np



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

cdata = get_covid_data()
len(cdata[0])

dates = sorted(list({ x['date'] for x in cdata[0]}))
dayOfPandemic={}
count=22
for d in dates:
    dayOfPandemic[d]=count
    count = count + 1



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

    
def averageData(L,k):
    """ average data over k days"""
    week = [0]*k
    newL=[]
    for x in L:
        week = week[1:]+[x[1]]
        newL += [(x[0],sum(week)/k)]
    return newL


def collectData(states,field,options={'perCapita':True,'averageByWeek':True}):
    """ 
        for a list of states and a field and an options object, return plottable data
        the data is a list of tuples (dayOfYear,value)  
        where the day of year goes from 1=1/1/2020 to 365=12/31/2020
    """
    perCapita = options['perCapita'] if 'perCapita' in options else False
    averageByWeek = options['averageByWeek'] if 'averageByWeek' in options else False
    if averageByWeek == True:
        averageByWeek=7
    pop=0
    for st in states:
        pop += statePop(st)
    data={}
    for d in cdata[0]:
        s=d['state']
        if s in states:
            n = getField(d,field)
            if d['date'] in data:
                data[d['date']] += n
            else:
                data[d['date']] = n
    z = sorted(data.items())
    if perCapita:
        z = [(dayOfPandemic[d[0]],d[1]*10000/pop) for d in z]
    else:
        z = [(dayOfPandemic[d[0]],d[1]) for d in z]
 

    if averageByWeek:
        z = averageData(z,averageByWeek)
        
    return z

def statePop(state):
    x = [d['Pop'] for d in stateData['data'] if state in states and d['State']==states[state]]
    return x[0] if len(x)>0 else 100000000

def plotItems(items,label):
    plt.rcParams['figure.figsize'] = [12, 6]
    """ plots the (day,value) pairs with the specified label"""
    plt.plot([x[0] for x in items],[x[1] for x in items],label=label)
    plt.xticks([0,30,60,90,120,150,180,210,240,270,300,330,360],'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec Jan'.split(' '))


def getField(x,field):
    if field in x:
        z = x[field]
        if (z==None):
            return 0
        else:
            return z
    else:
        return 0
def getStateData(state,field):
    sd = [(x['date'],getField(x,field)) for x in cdata[0] if x['state'] == state]
    return sorted(sd)

stateData = json.load(open("states.json","r"))

states = {
    "AL": "Alabama",
    "AK": "Alaska",
    #"AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    #"DC": "District Of Columbia",
    #"FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    #"GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    #"MH": "Marshall Islands",
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
    #"MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    #"PW": "Palau",
    "PA": "Pennsylvania",
    #"PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    #"VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

northEast   = ['MA','CT','RI','VT','NH','ME']
midAtlantic = ['NY','PA','NJ','DE','MD','VA','WV']
southEast   = ['NC','SC','GA','FL','AL','MS','LA','AR','TN']
southWest   = ['TX','OK','NM','CO','UT','AZ']
midWest     = ['OH','KY','IN','IL','MI','WI','MO','IA','MN','KS','NE','SD','ND']
west        = ['CA','NV','HI']
northWest   = ['WY','MT','ID','OR','WA','AK']

demStates = ['WA','OR','CA','NV','CO','NM',
            'MN','IL','VA','MD','DE','NJ',
            'NY','CT','RI','MA','VT','NH','ME','HI']

def otherStates(L):
    return [s for s in states.keys() if s not in L]

repStates = [s for s in states.keys() if s not in demStates]

def regionPop(states):
    pop=0
    for st in states:
        pop += statePop(st)
    return(pop)


if __name__ == '__main__':
    state = input("What state do you want to see?")
    (data,us) = get_covid_data()
    state_data = [d for d in data if d['state']==state]
    for r in state_data:
        print_info(r)
        print("\n*****************\n")
    print('bye!')
else:
    print('done')