from doctest import master
from unicodedata import category
import requests
import json
import time
import xml.etree.ElementTree as ET
import pika
import logging
from utilities import API_calls
from utilities import constants

IP = constants.IP

HEADERS={
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46ZWhiMTIz',
    'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
}

UID_HEADERS={
    'Content-type':'application/json', 
    'Accept':'application/json'
    }

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress Pika logs
pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.WARNING)


def publish_xml(xml_data, routing_key):
    connection = pika.BlockingConnection(pika.ConnectionParameters(IP, 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()

    exchange_name = "amq.topic"
    channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=xml_data)

    connection.close()


def get_stock():
    time.sleep(10)  # kies interval

    stock_url = f"http://{IP}:880/api/stock/"
    category_url = f"http://{IP}:880/api/part/category/"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }

    # Get the category data
    category_response = requests.request("GET", category_url, headers=headers, data=payload)
    category_data = category_response.json()

    # Mapping for categories
    category_mapping = {category["pk"]: category["pathstring"] for category in category_data}

    # Get the stock data
    response = requests.request("GET", stock_url, headers=headers, data=payload)
    data = response.json()

    new_item_found = False

    for item in data:
        part_id = item["part"]
        item_price_string = item["purchase_price"]
        item_price = round(float(item_price_string), 2)
        stock_id = item["pk"]

        # Get item info
        item_url = f"http://{IP}:880/api/part/{part_id}/"
        item_response = requests.request("GET", item_url, headers=headers, data=payload)
        item_data = item_response.json()
        item_name = item_data["name"]
        partUuid = item_data["description"]
        item_keyword = item_data.get("keywords", "").lower() if item_data.get("keywords") else ""

        # Category info
        category_id = item_data["category"]
        category = category_mapping.get(category_id, "")

        if partUuid == "":
            # New item
            partUuid = API_calls.create_part_masterUuid(part_id)
            API_calls.apply_partUuid(partUuid, part_id, category_id, item_name)
            item_data['description'] = partUuid
            item_data['category'] = category
            item_data['item_price'] = item_price  # Ensure 'item_price' is set
            logging.info(f"New item found: id: {part_id}, Name: {item_name}, Price: {item_price}, Category: {category}")
            print(f"New item found: id: {part_id}, Name: {item_name}, Price: {item_price}, Category: {category}, Description: {partUuid}")
            xml_data = create_product_xml(item_data)
            logging.info(xml_data)
            publish_xml(xml_data, "product.inventory")
            new_item_found = True
        elif "update" in item_keyword:
            # Updated item
            item_data['category'] = category
            item_data['item_price'] = item_price  # Ensure 'item_price' is set
            logging.info(f"Updated item found: id: {part_id}, Name: {item_name}, Price: {item_price}, Category: {category}")
            print(f"Updated item found: id: {part_id}, Name: {item_name}, Price: {item_price}, Category: {category}, Description: {partUuid}")
            xml_data = update_product_xml(item_data)
            logging.info(xml_data)
            publish_xml(xml_data, "product.inventory")
            update_item_keyword(part_id)
        elif "delete" in item_keyword:
            # Deleted item
            logging.info(f"Deleted item found: id: {part_id}, Name: {item_name}, Price: {item_price}, Category: {category}")
            print(f"Deleted item found: id: {part_id}, Name: {item_name}, Price: {item_price}, Category: {category}, Description: {partUuid}")
            xml_data = delete_product_xml(partUuid)
            logging.info(xml_data)
            publish_xml(xml_data, "product.inventory")
            delete_product_pk_in_masterUuid(partUuid)
            delete_stock(stock_id)
            delete_part(part_id)

    if not new_item_found:
        logging.info("No new items found...")


def create_product_xml(product):
    product_element = ET.Element("product")
    ET.SubElement(product_element, "routing_key").text = 'product.inventory'
    ET.SubElement(product_element, "crud_operation").text = 'create'
    ET.SubElement(product_element, "id").text = product['description']
    ET.SubElement(product_element, "name").text = product['name']
    ET.SubElement(product_element, "price").text = str(product['item_price'])
    ET.SubElement(product_element, "amount").text = None
    ET.SubElement(product_element, "category").text = product['category']
    ET.SubElement(product_element, "btw").text = None

    return ET.tostring(product_element, encoding='unicode')


def update_product_xml(product):
    product_element = ET.Element("product")
    ET.SubElement(product_element, "routing_key").text = 'product.inventory'
    ET.SubElement(product_element, "crud_operation").text = 'update'
    ET.SubElement(product_element, "id").text = product['description']
    ET.SubElement(product_element, "name").text = product['name']
    ET.SubElement(product_element, "price").text = str(product['item_price'])
    ET.SubElement(product_element, "amount").text = None
    ET.SubElement(product_element, "category").text = product['category']
    ET.SubElement(product_element, "btw").text = None

    return ET.tostring(product_element, encoding='unicode')


def delete_product_xml(uid):
    product_element = ET.Element("product")
    ET.SubElement(product_element, "routing_key").text = 'product.inventory'
    ET.SubElement(product_element, "crud_operation").text = 'delete'
    ET.SubElement(product_element, "id").text = uid
    ET.SubElement(product_element, "name").text = None
    ET.SubElement(product_element, "price").text = None
    ET.SubElement(product_element, "amount").text = None
    ET.SubElement(product_element, "category").text = None
    ET.SubElement(product_element, "btw").text = None

    return ET.tostring(product_element, encoding='unicode')

def update_item_keyword(part_id, new_keyword=""):
    item_url = f"http://{IP}:880/api/part/{part_id}/"
    payload = {"keywords": new_keyword}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
    }
    response = requests.patch(item_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        logging.info(f"Updated keyword for part_id {part_id} to '{new_keyword}'")
    else:
        logging.error(f"Failed to update keyword for part_id {part_id}: {response.status_code}, {response.text}")

def delete_product_pk_in_masterUuid(uid):
    #MasterUuid
    masterUuid_url = f"http://{IP}:6000/updateServiceId"
    masterUuid_payload = json.dumps(
        {
            "MASTERUUID": f"{uid}",
            "Service": "inventory",
            "ServiceId": "NULL"
        }
    )
    print(f"uid: {uid}")
    print("Pk has been deleted")
    return requests.request("POST", masterUuid_url, headers=UID_HEADERS ,data=masterUuid_payload)

def delete_stock(stock_pk):
    url = f"http://{IP}:880/api/stock/{stock_pk}/"
    payload={}
    return requests.request("DELETE", url, headers=HEADERS, data=payload)

def delete_part(product_pk):
    url = f"http://{IP}:880/api/part/{product_pk}/"
    payload={}
    return requests.request("DELETE", url, headers=HEADERS, data=payload)

while True:
    get_stock()
