# -*- coding: utf-8 -*-
import requests, json

key = 'AIzaSyDMvd2ybB24ssqr1GmPYwUHWT_0cewKfDE'
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
query = input('Search query: ')

r = requests.get(url + 'query=' + query +
                        '&key=' + key)
x=r.json()
y = x['results']
for i in range(len(y)):
    print(y[i]['name'])