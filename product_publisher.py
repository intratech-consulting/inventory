from doctest import master
from unicodedata import category
import requests
import json
import time
import xml.etree.ElementTree as ET
import pika
import logging
from utilities import API_calls

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress Pika logs
pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.WARNING)



def publish_xml(xml_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.53', 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()

    exchange_name = "amq.topic"
    channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

    channel.basic_publish(exchange=exchange_name, routing_key='product.inventory', body=xml_data)

    connection.close()

def get_stock():
    time.sleep(30) ### kies interval ###

    stock_url = "http://10.2.160.53:880/api/stock/"
    category_url = "http://10.2.160.53:880/api/part/category/"
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
        item_url = f"http://10.2.160.53:880/api/part/{part_id}/"
        item_response = requests.request("GET", item_url, headers=headers, data=payload)
        item_data = item_response.json()
        item_name = item_data["name"]
        partUuid = item_data["description"]


        #categorie info
        category_id = item_data["category"]
        category = category_mapping.get(category_id, "")

        if partUuid == "":
            partUuid = API_calls.create_part_masterUuid(part_id)
            API_calls.apply_partUuid(partUuid, part_id, category_id, item_name)
            item = Item(part_id, item_name, item_price, category, partUuid)
            logging.info(f"Nieuw item gevonden: id: {part_id}, Naam: {item_name}, Price: {item_price}, Categorie: {category}")
            print(f"Nieuw item gevonden: id: {part_id}, Naam: {item_name}, Price: {item_price}, Categorie: {category}, Description: {partUuid}")
        # if part_id not in [item.part_id for item in product_list]:
        #     #als item niet in de lijst is, toevoegen
        #     product_list.append(item)
            xml_data = create_xml(item)
            logging.info(xml_data)
            publish_xml(xml_data) # Publisher voor kassa komt hier!!! #
            new_item_found = True

    if not new_item_found:
        logging.info("Geen nieuwe items gevonden...")

    #for item in product_list:
    #    print(f"ID: {item.part_id}, Name: {item.item_name}, Price: {item.item_price}, Category: {item.category}")


class Item():
    def __init__(self, part_id, item_name, item_price, category, partUuid):
        self.routing_key = "product.inventory"
        self.crud_operation = "create"
        self.part_id = part_id
        self.item_name = item_name
        self.item_price = item_price
        self.category = category
        self.amount = "-1"
        self.btw = "-1"
        self.description = partUuid

def create_xml(item: Item):
    product = ET.Element("product")
    ET.SubElement(product, "routing_key").text = "product.inventory"
    ET.SubElement(product, "crud_operation").text = "create"
    ET.SubElement(product, "id").text = str(item.description)
    ET.SubElement(product, "name").text = str(item.item_name)
    ET.SubElement(product, "price").text = str(item.item_price)
    ET.SubElement(product, "amount").text = str(item.amount)
    ET.SubElement(product, "category").text = str(item.category)
    ET.SubElement(product, "btw").text = str(item.btw)

    xml_data = ET.tostring(product, encoding="unicode", method="xml")
    return xml_data

while True:
    get_stock()
