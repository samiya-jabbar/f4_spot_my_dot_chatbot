import requests

url = 'http://aiderma.ew.r.appspot.com/create_account'
myobj = {'userid':'samiya.python@gmail.com',
    'pwd': 'abcdefg',
    'name' : 'sana',
    'age': '23', 
    'image of individual': 'a.jpeg', 
    'blood pressure' : '77'}
x = requests.post(url, data = myobj)
print(x.text)