import requests
import json

class PostsLoader():
  def __init__(self, ids):
      self.user_ids = ids
      self.index = 0
      self.method = 'wall.get'
      self.api_url = 'https://api.vk.com/method/'
      self.access_token  = ''
      self.v = '5.131'
      self.params = {
        'access_token' : self.access_token,
        'v' : self.v
      }

  def next(self):
    if self.index < len(self.user_ids):
      local_params = {
        'owner_id' : self.user_ids[self.index]
      }
      self.index += 1
      res = requests.get(self.api_url + self.method, params={**local_params, **self.params})
      
      if ('response' in res.json()):
        return res.json()['response']['items']

