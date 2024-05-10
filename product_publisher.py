from unicodedata import category
import requests
import json
import time
import xml.etree.ElementTree as ET
import pika

product_list = []

def establish_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))
    return connection

def publish_xml(xml_data):
    connection = establish_connection()
    channel = connection.channel()

    exchange_name = "amq.topic"
    channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

    channel.basic_publish(exchange=exchange_name, routing_key='product.inventory', body=xml_data)

    print(" [x] Sent test order message")

    connection.close()

def get_stock():
    global product_list

    stock_url = "http://10.2.160.51:880/api/stock/"
    category_url = "http://10.2.160.51:880/api/part/category/"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }

    #get de categorie data
    category_response = requests.request("GET", category_url, headers=headers, data=payload)
    category_data = category_response.json()

    #mapping voor categorie
    category_mapping = {category["pk"]: category["pathstring"] for category in category_data}

    #get de stock data
    response = requests.request("GET", stock_url, headers=headers, data=payload)
    data = response.json()

    new_item_found = False

    for item in data:
        part_id = item["part"]
        item_price_string = item["purchase_price"]
        item_price = round(float(item_price_string), 2)
        #get item info
        item_url = f"http://10.2.160.51:880/api/part/{part_id}/"
        item_response = requests.request("GET", item_url, headers=headers, data=payload)
        item_data = item_response.json()
        item_name = item_data["name"]


        #categorie info
        category_id = item_data["category"]
        category = category_mapping.get(category_id, "")

        if part_id not in product_list:
            #als item niet in de lijst is, toevoegen



            item = Item(part_id, item_name, item_price, category)
            product_list.append(item)
            print(f"Nieuw item gevonden: id: {part_id}, Naam: {item_name}, Price: {item_price}, Categorie: {category}")
            xml_data = create_xml(item)
            print(xml_data)
            publish_xml(xml_data) # Publisher voor kassa komt hier!!! #
            new_item_found = True

    if not new_item_found:
        print("Geen nieuwe items gevonden...")

    #for item in product_list:
    #    print(f"ID: {item.part_id}, Name: {item.item_name}, Price: {item.item_price}, Category: {item.category}")

    time.sleep(30) ### kies interval ###

class Item():
    def __init__(self, part_id, item_name, item_price, category):
        self.part_id = part_id
        self.item_name = item_name
        self.item_price = item_price
        self.category = category
        self.total = "-1"
        self.totalExBtw = "-1"
        self.amount = "-1"
        self.btw = "-1"

def create_xml(item: Item):
    product = ET.Element("product")
    ET.SubElement(product, "id").text = str(item.part_id)
    ET.SubElement(product, "name").text = str(item.item_name)
    ET.SubElement(product, "price").text = str(item.item_price)
    ET.SubElement(product, "amount").text = str(item.amount)
    ET.SubElement(product, "category").text = str(item.category)
    ET.SubElement(product, "total").text = str(item.total)
    ET.SubElement(product, "total_ex_btw").text = str(item.totalExBtw)
    ET.SubElement(product, "btw").text = str(item.btw)

    xml_data = ET.tostring(product, encoding="unicode", method="xml")
    return xml_data


while True:
    get_stock()