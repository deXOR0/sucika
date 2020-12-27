import requests

aktivis = open('aktivis.csv')

content = aktivis.read().splitlines()

for c in content:
    name, msg = c.split(';')
    print(requests.get(r'http://127.0.0.1:5000/createSucika?name={}&msg={}'.format(name, msg)))