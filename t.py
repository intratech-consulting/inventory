
import pika
import xml.etree.ElementTree as ET
import requests
import json

user_data = {
        'user_id': "5",
        'first_name': "bob",
        'last_name': "bobette",
        'email': "yay.be@hotmail.be",
        'telephone': "123456",
        'company': "hilo",
        'company_id': "5",
        'user_role': "speaker"
    }

array=[]
array.append( user_id='5')
# print(f"Company name is:{user_data['company']} \n Company id is:{user_data['company_id']}\n User role is: {user_data['user_role']}")
print(array[0])