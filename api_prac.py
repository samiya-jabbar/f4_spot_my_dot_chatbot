import requests
import json
"""
url = 'http://aiderma.ew.r.appspot.com/create_account'
myobj = {'userid':'samiya.python@gmail.com',
    'pwd': 'abcdefg',
    'name' : 'sana',
    'age': '23', 
    'image of individual': 'a.jpeg', 
    'blood pressure' : '77'}
x = requests.post(url, data = myobj)
print(x.text)

"""
url = 'http://aiderma.ew.r.appspot.com/fetch_metadata'
#userid = req.get('queryResult').get('parameters').get('userid')
#print(userid)
userid = 'anumta@gmail.com'
myobj = {'userid' : userid }
x = requests.post(url, data = myobj)
x = x.text
print(x)
result = json.loads(x)
print(result['metadata']['name'])









