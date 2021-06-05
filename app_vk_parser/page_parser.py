import requests
import time
import json
from datetime import date, datetime
import re


accessToken = ''

api_url = 'https://api.vk.com/method/'

NUM_OF_USERS = 50

app_params = {
  'access_token' : accessToken,
  'v' : '5.131'
}

def process_raw_str(string):
  return re.sub(r'[\W]', ' ', string).lower()

'''
  Сначала получаем всех пользователей
'''
def fetchUsers():
  user_ids = []
  method = 'groups.getMembers'

  local_params = {
    # 'group_id' : 'beryozoviy_markova',
    'group_id' : '174834195'
  }
  res = requests.get(api_url + method, params={**app_params, **local_params})
  ids = res.json()['response']['items']
  return ids

'''
Собираем по ним данные
'''
def parsePages(ids):
  method = 'users.get'
  local_params = {
    'user_ids' : ','.join(map(str,ids[:NUM_OF_USERS])),
    'fields' : ', '.join(['activities', 'interests', 'bdate', 'occupation', 'sex'])
  }
  
  res = requests.get(api_url + method, params={**app_params, **local_params})
  data = res.json()['response']

  '''
    Считвыаем возраст, если возраст не указан - пытаемся угадать,
    исходя из места работы
  '''
  for item in data:
    if not 'bdate' in item:
      if 'occupation' in item and item['occupation']['type'] == 'university':
        item['age'] = 20
      else:
        item['age'] = None
    else:
      dateSplit = item['bdate'].split('.')
      if len(dateSplit) == 3:
        item['age'] = datetime.now().year - int(item['bdate'].split('.')[2])
      else:
        item['age'] = None
  return data


'''
Находим id групп, в которых они состоят
'''
def fetchGroups(people):

    for p in people:
      p['groups'] = []
      if 'is_closed' in p and not p['is_closed']:
        method = 'groups.get'
        local_params = {
          'user_id' : p['id']
        }
        res = requests.get(api_url + method, params={**app_params, **local_params})
        groups = res.json()

        if 'response' in groups:
          groups = groups['response']['items']
        
          for group in groups:
            method = 'groups.getById'
            local_params = {
              'group_id': group,
              'fields' : ','.join(['description', 'activity'])
            }
            res = requests.get(api_url + method, params={**app_params, **local_params})
            g_data = res.json()
            if 'response' in g_data:
              r = g_data['response'][0]
              g = {}
              if 'activity' in r:
                g['activity'] = r['activity']
              if 'description' in r:
                g['description'] = r['description']
              g['id'] = r['id']
              g['name'] = r['name']
              p['groups'].append(g)
          
        time.sleep(0.6)
    
            







ids = fetchUsers()
people = parsePages(ids)
fetchGroups(people)
print(people)

aggregates = {
  'age_agg' : {},
  'groups_agg' : {},
  'working_agg': 0,
  'activities' : {},
  'interests': {}
}
 
# for item in people:
#  if 'age' in item and item['age'] in aggregates['age_agg']:
#    aggregates['age_agg'][item['age']] += 1
#  elif 'age' in item and item['age'] not in aggregates['age_agg']:
#    aggregates['age_agg'][item['age']] = 1

#  if 'interests' in item and item['interests'] != '':
#     interests = item['interests'].split(', ')
#     for intrst in interests:
#       if intrst in aggregates['interests']:
#         aggregates['interests'][intrst] += 1
#       else:
#         aggregates['interests'][intrst] = 1

# if 'groups' in item and len(item['groups']) != 0:
#   for group in item['groups']:
#     g = process_raw_str(group['name'])

#     if g in aggregates['groups_agg']:
#       aggregates['groups_agg'][g] += 1
#     else:
#       aggregates['groups_agg'][g] = 1

# if 'occupation' in item and item['occupation']['type'] == 'work':
#   aggregates['working_agg'] += 1

# if 'activities' in item and len(item['activities']) != 0:
#   activities = item['activities'].split(', ')
#   for a in activities:
#     if a in aggregates['activities']:
#       aggregates['actvities'][a] += 1
#     else:
#       aggregates['activities'][a] = 1

# aggregates['working_agg'] /= len(people)

# print(aggregates['activities'])

# for p in people:
  # if 'activities' in p:
  #   print(p['activities'])
  #   print()
  # if 'interests' in p:
  #   f.write(p['interests'])
  # if 'groups' in p:
  #   print(p['groups'])
  #   print()

data = json.dumps(people)

f = open("murino.json", "w")
f.write(data)
f.close()

