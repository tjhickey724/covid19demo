# covid19demo
This is a Jupyter lab demo to visualize the data from http://covidtracking.com



## Running the Jupyter notebook code
You can  run the Jupyter notebook code by downloading this repository, cd'ing to the jupyterdemo folder
and giving the command
``` linux
% jupyter lab
```
You will have to have installed the Jupyter lab modules... Google is your friend, ask her how to do it!

## covid19.py package
The covid19.py module defines several functions to help you create visualizations using matplotlib
We list them below:

''' python
getCovidData()
'''
This visits the two URLs for the daily historical data for the individual states and the US as a whole
https://covidtracking.com/api/states/daily
https://covidtracking.com/api/us/daily
and converts them from JSON to python. It returns a list of two elements [stateData,usData]
each of these is a list of Python objects and you can get the keys using
''' python
data = get_covid_data()
statedatum = data[0][0]
usdataum = data[1][0]
print("state keys")
print(list(statedatum))
print("us keys")
print(list(data[1][0]))
'''
As of 7/20/2020 the state keys are

['date', 'state', 'positive', 'negative', 'pending', 'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently', 'inIcuCumulative', 'onVentilatorCurrently', 'onVentilatorCumulative', 'recovered', 'dataQualityGrade', 'lastUpdateEt', 'dateModified', 'checkTimeEt', 'death', 'hospitalized', 'dateChecked', 'totalTestsViral', 'positiveTestsViral', 'negativeTestsViral', 'positiveCasesViral', 'deathConfirmed', 'deathProbable', 'fips', 'positiveIncrease', 'negativeIncrease', 'total', 'totalTestResults', 'totalTestResultsIncrease', 'posNeg', 'deathIncrease', 'hospitalizedIncrease', 'hash', 'commercialScore', 'negativeRegularScore', 'negativeScore', 'positiveScore', 'score', 'grade']

and the US keys are

['date', 'states', 'positive', 'negative', 'pending', 'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently', 'inIcuCumulative', 'onVentilatorCurrently', 'onVentilatorCumulative', 'recovered', 'dateChecked', 'death', 'hospitalized', 'lastModified', 'total', 'totalTestResults', 'posNeg', 'deathIncrease', 'hospitalizedIncrease', 'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease', 'hash']
​

Covid-19 also defines a function to get the data for a particular field possibly perCapita and/or averaged by Week:

''' python
def collectData(states,field,options={'perCapita':True,'averageByWeek':True}):
'''
e.g.
''' python
data = collectData(['MA'],'positiveIncrease',options={'perCapita':False,'averageByWeek':False})
data[-10:]

[(192, 213),
 (193, 288),
 (194, 199),
 (195, 230),
 (196, 303),
 (197, 217),
 (198, 234),
 (199, 298),
 (200, 359),
 (201, 296)]
'''

Another useful function plots the items with the horizontal scale being the days of 2020
''' python
plotItems(
    collectData(s,
                'positiveIncrease',
                options={'perCapita':False,'averageByWeek':False}),
    'new cases per 10K')
'''
