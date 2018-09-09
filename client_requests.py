import requests
import json
import datetime as dt

payload = {
     'fullname': 'valera safonik',
     'email': 'saffff@ukr.net',
     'nickname': 'saffff',
     'birthday': '2014-12-22',
     'password': '12345',
     'phone': '+380968813311',
     'invited_type': 'personal',
     'invited_by': '5a32ba1bfa3b3062bb7218a1',
     'skills': ['Customer Experience'],
     'interests': ['Video Games'],
     'industry': {
          'industry': 'Telecommunications',
          'experience': 5,
     },
     'current_location': {
          'google_place_city_id': 12345,
          'city_name': 'Kyiv',
          'country_name': 'Ukraine',
     },
}
files = {
     'json': (None, json.dumps(payload), 'application/json'),
     'photo': ('1.jpg', open('/home/safonik/Downloads/1.jpg', 'rb'), 'image/jpeg')
}

r = requests.post('http://0.0.0.0:8000/api/v2/registry/', files=files)

print(r.content)
