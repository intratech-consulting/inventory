import time
import xml.etree.ElementTree as ET
import pika
import json
from utilities import API_calls  # Import API calls module
from utilities import functions  # Import functions module

IP='10.2.160.51'

# Function to that makes a payload to update the user without description(user made is ui)
def get_payload_to_update_user(first_name,last_name,user,uid):
    user_name=name=first_name+'.'+last_name
    phone=user['phone']
    email=user['email']

    payload = json.dumps(
            {
                "name": user_name,
                "phone": phone,
                "email": email,
                "description": uid,
                "currency": "EUR",
                "contact":None,
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False,
            }
        )
    return payload

# Function that creates the XML to create an user and returns it
def create_xml(user):
    name=user['name']
    name_array=name.split(".")
    user_element = ET.Element("user")

    #Creates uid for new user
    uid=API_calls.create_user_masterUuid(user["pk"])
   
    ET.SubElement(user_element, "routing_key").text = 'user.inventory'
    ET.SubElement(user_element, "crud_operation").text = 'create'
    ET.SubElement(user_element, "id").text = uid
    ET.SubElement(user_element, "first_name").text = name_array[0]
    ET.SubElement(user_element, "last_name").text = name_array[1]
    ET.SubElement(user_element, "email").text = user['email']
    ET.SubElement(user_element, "phone").text = user['phone']
    ET.SubElement(user_element, "birthday").text = None
       
    address_element = ET.SubElement(user_element, "address")
    ET.SubElement(address_element, "country").text = None
    ET.SubElement(address_element, "state").text = None
    ET.SubElement(address_element, "city").text = None
    ET.SubElement(address_element, "zip").text = None
    ET.SubElement(address_element, "street").text = None
    ET.SubElement(address_element, "house_number").text = None
 
    ET.SubElement(user_element, "company_email").text = None
    ET.SubElement(user_element, "company_id").text = None
    ET.SubElement(user_element, "source").text = None
    ET.SubElement(user_element, "user_role").text = None
    ET.SubElement(user_element, "invoice").text = None
    ET.SubElement(user_element, "calendar_link").text = None

    # Get payload to update the newly created user in the ui
    payload=get_payload_to_update_user(name_array[0],name_array[1],user,uid)

    # Updates user in the database
    API_calls.update_user(payload,user["pk"])

    xml_data = ET.tostring(user_element, encoding="unicode")
    print(f"xml_data: {xml_data}")
    return xml_data

# Function that returns the list of users in inventree
def fetch_users():
    response = API_calls.get_users()
    users = response.json()
    print(f"fetching is done")
    return users
 
# Function that enables us to publish messages on the queue
def publish_to_queue(xml_data):
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(IP, 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()
 
    # Declare the exchange
    exchange_name = "amq.topic"
    routing_key = 'user.inventory'
    channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)
 
    # Publish XML to RabbitMQ
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=xml_data)
 
    print("Nieuwe user gepublished")
    # Close connection
    connection.close()

# Function that creates the XML to update an user and returns it
def f_update_xml(existing_user, updated_user, updated_fields: list):
    payload={}
    user_element = ET.Element("user")
    ET.SubElement(user_element, "routing_key").text = "user.inventory"
    ET.SubElement(user_element, "crud_operation").text = "update"
    ET.SubElement(user_element, "id").text = existing_user['description']

    if updated_fields[0]is not None and updated_fields[1]is not None:
        new_name_array=updated_user["name"].split(".")         
        ET.SubElement(user_element, "first_name").text = new_name_array[0]
        ET.SubElement(user_element, "last_name").text = new_name_array[1]

        payload['name']=updated_user["name"]
    
    if updated_fields[0]is None and updated_fields[1]is not None:
        new_name_array=updated_user["name"].split(".")
        old_name_array=existing_user["name"].split(".")          
        ET.SubElement(user_element, "first_name").text = old_name_array[0]
        ET.SubElement(user_element, "last_name").text = new_name_array[1]

        payload['name']=old_name_array[0]+'.'+new_name_array[1]

    if updated_fields[0]is None and updated_fields[1]is None:         
        ET.SubElement(user_element, "first_name").text = None
        ET.SubElement(user_element, "last_name").text = None
    
    if updated_fields[0]is not None and updated_fields[1]is None:
        new_name_array=updated_user["name"].split(".")
        old_name_array=existing_user["name"].split(".")          
        ET.SubElement(user_element, "first_name").text = new_name_array[0]
        ET.SubElement(user_element, "last_name").text = old_name_array[1]

        payload['name']=new_name_array[0]+'.'+old_name_array[1]

    if updated_fields[2] is None:
        ET.SubElement(user_element, "email").text = None
    if updated_fields[3] is None:
        ET.SubElement(user_element, "phone").text = None

    for field in updated_fields:
        if field == "email":
            if updated_user['email'] is not None:
                ET.SubElement(user_element, "email").text = updated_user['email']
                payload["email"]=updated_user['email']
        elif field == "phone":
            if updated_user['phone'] is not None:
                ET.SubElement(user_element, "phone").text = updated_user['phone']
                payload["phone"]=updated_user['phone']
        ET.SubElement(user_element, "birthday").text = None

    payload['contact']=''
    payload['currency']='EUR'
       
    address_element = ET.SubElement(user_element, "address")
    ET.SubElement(address_element, "country").text = None
    ET.SubElement(address_element, "state").text = None
    ET.SubElement(address_element, "city").text = None
    ET.SubElement(address_element, "zip").text = None
    ET.SubElement(address_element, "street").text = None
    ET.SubElement(address_element, "house_number").text = None
 
    ET.SubElement(user_element, "company_email").text = None
    ET.SubElement(user_element, "company_id").text = None
    ET.SubElement(user_element, "source").text = None
    ET.SubElement(user_element, "user_role").text = None
    ET.SubElement(user_element, "invoice").text = None
    ET.SubElement(user_element, "calendar_link").text = None

    API_calls.update_user(payload,updated_user['pk'])
 
    xml_data = ET.tostring(user_element, encoding="unicode")

    return xml_data

# Function that checks the changes
def handle_user_update(existing_user, updated_user):

    #Empty array to be filled
    updated_fields = []

    # Extract first name and last name from the company_name field
    existing_user_name_array=existing_user['name'].split('.')
    updated_user_name_array=updated_user['name'].split('.')
    
    # Pasting the first & last names into variables
    existing_first_name = existing_user_name_array[0]
    existing_last_name = existing_user_name_array[1]
    updated_first_name = updated_user_name_array[0]
    updated_last_name =  updated_user_name_array[1]
 
    # Checking if there is a change, if so place the field into the array, if not place None into the array
    if existing_first_name != updated_first_name:
        updated_fields.append("first_name")
    else:
        updated_fields.append(None)

    if existing_last_name != updated_last_name:
        updated_fields.append("last_name")
    else:
        updated_fields.append(None)

    if existing_user['email'] != updated_user['email']:
        updated_fields.append("email")
    else:
        updated_fields.append(None)

    if existing_user['phone'] != updated_user['phone']:
        updated_fields.append("phone")
    else:
        updated_fields.append(None)
 
    # If any of the tracked fields have been updated, create and publish update XML
    if updated_fields:

        # Calls function to create the update XML
        update_xml = f_update_xml(existing_user, updated_user, updated_fields)

        # Publish the updated user to the queue
        publish_to_queue(update_xml)
    else:
        print("No relevant changes detected for the user.")
 
# Function that creates the XML to delete a user and returns it
def f_delete_xml(user_uid: str):

    # Creating the body
    user_element = ET.Element("user")
    ET.SubElement(user_element, "routing_key").text = "user.inventory"
    ET.SubElement(user_element, "crud_operation").text = "delete"
    ET.SubElement(user_element, "id").text = user_uid
    # Set all other fields to None
    ET.SubElement(user_element, "first_name").text = None
    ET.SubElement(user_element, "last_name").text = None
    ET.SubElement(user_element, "email").text = None
    ET.SubElement(user_element, "phone").text = None
    ET.SubElement(user_element, "birthday").text = None
    address_element = ET.SubElement(user_element, "address")
    ET.SubElement(address_element, "country").text = None
    ET.SubElement(address_element, "state").text = None
    ET.SubElement(address_element, "city").text = None
    ET.SubElement(address_element, "zip").text = None
    ET.SubElement(address_element, "street").text = None
    ET.SubElement(address_element, "house_number").text = None
    ET.SubElement(user_element, "company_email").text = None
    ET.SubElement(user_element, "company_id").text = None
    ET.SubElement(user_element, "source").text = None
    ET.SubElement(user_element, "user_role").text = None
    ET.SubElement(user_element, "invoice").text = None
    ET.SubElement(user_element, "calendar_link").text = None
    xml_data = ET.tostring(user_element, encoding="unicode")

    return xml_data

#Handles the user delete
def handle_user_delete(deleted_user_uid: str):

    # Calls function to create an XML file
    delete_xml = f_delete_xml(deleted_user_uid)

    # Publishes the the deleted user to the queue
    publish_to_queue(delete_xml)
 
def main():
    # Initialize array list to store users
    users_list = []
   
    # Fetch initial users
    users_list = fetch_users()

    # flag for if there was a change
    change=False

    while True:
        
        # Fetch updated users after 60 seconds
        time.sleep(60)

        # Fetches all the users in the database
        updated_users = fetch_users()

        # Check for new users, updated users, and deleted users
        for updated_user in updated_users:
            if updated_user['description'] == "":
                change=True

                # New user detected
                user_xml = create_xml(updated_user)

                # Publishe the new user to the queue
                publish_to_queue(user_xml)

                # Adds the new user to the list
                users_list.append(updated_user)
            elif updated_user['contact']=='update':

                # Get the old user json object
                old_user=functions.get_user_with_same_uid(updated_user['description'], users_list)

                # Handles the user to be updated
                handle_user_update(old_user, updated_user)

                # Update user in the list
                users_list.append(updated_user)
                users_list.remove(old_user)



                change=True
            elif updated_user['contact']=='delete':
                old_user=functions.get_user_with_same_uid(updated_user['description'], users_list)

                handle_user_delete(old_user['description'])

                API_calls.delete_user(updated_user['pk'])

                users_list.remove(old_user)

                change=True

        
        # Loop old user through new list to find user with same Uuid, if not found it means it has been deleted
        for old_user in users_list:

            # Function that checks if the old user is in the new list
            if functions.find_user_in_list(updated_users, old_user):

                # Handles the user to be deleted
                handle_user_delete(old_user['description'])

                change=True

                # Removes the old user from the list
                users_list.remove(old_user)
            
        if change==False:
            print("Nothing new")
        
 
 
if __name__ == "__main__":
    main()


