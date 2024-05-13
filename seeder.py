import xml.etree.ElementTree as ET
import xmlrpc.client
import pika
import requests
import json
import random


IP="http://10.2.160.51:"
def create_category(category_name,parent_category_id = ""):
    url = f"{IP}880/api/part/category/"
    if parent_category_id == "":
        payload = json.dumps({
        "name":category_name
    })
    else:
        payload = json.dumps({
            "name":category_name,
            "parent": parent_category_id
        })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def create_part(part_name, category_id):
    url = f"{IP}880/api/part/"
    payload = json.dumps({
        "name":part_name,
        "category": category_id,
        "minimum_stock":1
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def create_stock(part_id,quantity,purchase_prise):
    url = f"{IP}880/api/stock/"
    payload = json.dumps({
        "part":part_id,
        "quantity": quantity,
        "purchase_price":purchase_prise,
        "purchase_price_currency":"EUR"
    })
    # currency best een ENUM
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

# create_category("nurriture",5)
#create_part("peren",6)
#create_stock(8,100,20)

cold_drink_list = ["Coca-Cola", "Sprite", "Fanta", "Iced-Tea", "Iced-Coffee", "Orange Juice"]
hot_drink_list = ["Mint Tea", "Hot Chocolate", "Espresso", "Cappuccino", "Latte", "Mocha"]

snack_list = ["Chips", "Cookies", "Popcorn", "Crackers"]
sandwich_list = ["Grilled Cheese", "Tuna Salad", "Vegetarian", "Chicken Caesar", "Ham and Cheese"]
fruit_list = ["Apples", "Bananas", "Grapes", "Strawberries", "Pineapple", "Watermelon", "Kiwi"]

def seeder():
    create_category("Drinks")          #id  #1
    create_category("Cold Drinks", 1)  #id  #2
    create_category("Hot Drinks", 1)   #id  #3

    create_category("Food")            #id  #4
    create_category("Snacks", 4)       #id  #5
    create_category("Sandwiches", 4)   #id  #6
    create_category("Fruit", 4)        #id  #7

    x = 1
    for drink in cold_drink_list:
        create_part(drink, 2)
        create_stock(x, random.randint(300, 400), round(random.uniform(1.5, 2.5), 2))
        x += 1
    
    for drink in hot_drink_list:
        create_part(drink, 3)
        create_stock(x, random.randint(300, 400), round(random.uniform(2.0, 3.0), 2))
        x += 1
    
    for snack in snack_list:
        create_part(snack, 5)
        create_stock(x, random.randint(300, 400), round(random.uniform(0.7, 2.0), 2))
        x += 1
    
    for sandwich in sandwich_list:
        create_part(sandwich, 6)
        create_stock(x, random.randint(300, 400), round(random.uniform(3.0, 4.5), 2))
        x += 1
    
    for fruit in fruit_list:
        create_part(fruit, 7)
        create_stock(x, random.randint(300, 400), round(random.uniform(1.0, 2.0), 2))
        x += 1





































# # connect to odoo database
# url = "http://10.2.160.51:8069/"
# user = "desiderius.hackathon@ehb.be"
# password = "7VJ0TSB4ft9"
# db = "dbodoo"
 
# common = xmlrpc.client.ServerProxy(url+"/xmlrpc/common")
# user = common.login(db, user, password)
 
# print(f"auth and the id is : {user}")
 
# model = "product.template"
 
# search = []
 
# operation = xmlrpc.client.ServerProxy(url+"/xmlrpc/object")
 
# method = "search_read"
# list_of_products = operation.execute(db, user, password, model, method, search, ["id", "name", "list_price", "categ_id"])
# for product in list_of_products:
#     print(product)
 
 
# product_with_id = next((product for product in list_of_products if product['id'] == 10), {})
 
# if product_with_id:
#     product_template_id = product_with_id.get("id", "")
#     product_template_name = product_with_id.get("name","")
#     product_template_price = product_with_id.get("list_price", "")
#     product_template_category_id = product_with_id.get("categ_id", "")
 
#     print("Name of partner with ID 1:", product_template_name)
# else:
#     print("No partner found with ID 1")
 
 
# # Construct XML as a string
# xml_data = f"""<product>
#     <routing_key>product.crm</routing_key>
#     <crud_operation>create</crud_operation>
#     <id>{product_template_id}</id>
#     <name>{product_template_name}</name>
#     <price>{product_template_price}</price>
#     <amount>3</amount>
#     <category>{product_template_category_id}</category>
#     <btw>0.50</btw>
# </product>"""
 
 
# # Write XML string to file
# with open("product_data.xml", "w") as file:
#     file.write(xml_data)
 
# print("XML file saved as user_data.xml")