# -*- coding: utf-8 -*-
import requests, json
from transliterate import translit
key = 'AIzaSyDMvd2ybB24ssqr1GmPYwUHWT_0cewKfDE'
keyVk = '057e5b74d5c1e0c4583eb3cebf7ee8e59f89a56580d9a8c134dff7e64c4aab296bd7994eec7d2bdecb911'
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
urlVk='https://api.vk.com/method/groups.search?'
query = input('Search query: ')
forVk=[]

r = requests.get(url + 'query=' + query +
                        '&key=' + key)
x = r.json()
y = x['results']
for i in range(len(y)):
    ru_text = translit(y[i]['name'], 'ru')
    rVk = requests.get(urlVk + 'q=' + ru_text +
                       '&count=1' +
                       '&access_token=' + keyVk +
                       '&v=5.131')
    x2 = rVk.json()
    y2 = x2['response']
    z=y2['items']
    for j in range(len(z)):
        forVk.append(z[j]['screen_name'])
print(forVk)
