import requests
import json
import time

product_list = []

def get_stock():
    global product_list

    url = "http://inventree.localhost/api/stock/"
    category_url = "http://inventree.localhost/api/part/category/"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cm9vdDpxdWVudGluMTIz',
        'Cookie': 'csrftoken=U4f3aiFMtXqeenAz6du2wfmD9e5ymh1K; sessionid=fnoffjbzoqhv66k0n1zonlsjt0qoqrzv'
    }

    #get de categorie data
    category_response = requests.request("GET", category_url, headers=headers, data=payload)
    category_data = category_response.json()

    #mapping voor categorie
    category_mapping = {category["pk"]: category["pathstring"] for category in category_data}

    #get de stock data
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    new_item_found = False

    for item in data:
        part_id = item["part"]

        #get item info
        item_url = f"http://inventree.localhost/api/part/{part_id}/"
        item_response = requests.request("GET", item_url, headers=headers, data=payload)
        item_data = item_response.json()
        item_name = item_data["name"]

        #categorie info
        category_id = item_data["category"]
        category_path = category_mapping.get(category_id, "")
        
        if part_id not in product_list:
            #als item niet in de lijst is, toevoegen

            # Publisher voor kassa komt hier!!! #

            product_list.append(part_id)
            print(f"Nieuw item gevonden: id: {part_id}, Naam: {item_name}, categorie: {category_path}")
            new_item_found = True

    if not new_item_found:
        print("Geen nieuwe items gevonden...")

    time.sleep(999) ### kies interval ###

while True:
    get_stock()
