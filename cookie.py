import requests
import os

url = "http://inventree.localhost/index/"
data = {}
header = {"Content-Type": "application/json"}
client=requests.Session()
client.get(url)
x = requests.post(url, json=data, headers=header)
print(x.cookies.get_dict())