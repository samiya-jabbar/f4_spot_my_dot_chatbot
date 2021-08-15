import requests

url = 'http://aiderma.ew.r.appspot.com/auth_account'
myobj = {'userid':'samiaj638@gmail.com', 'pwd': '123456'}
x = requests.post(url, data = myobj)
print(x.text)