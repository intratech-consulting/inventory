import time
import xml.etree.ElementTree as ET
import pika
import lxml
from lxml import etree
import json
import logging
from utilities import API_calls  # Import API calls module
from utilities import functions  # Import functions module
from utilities import xmls
from utilities import xsds
from utilities import constants
import datetime
from datetime import datetime
import requests

IP=constants.IP
USER_XSD=xsds.get_user_xsd()


# Create a logger
logger = logging.getLogger("INFO")
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

# Define the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the console logging level to INFO
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

# Function that creates the XML to create an user and returns it
def create_xml(user):
    
    uid=API_calls.create_user_masterUuid(user["pk"])
    #Creates uid for new user
    user_xml_str= xmls.create_user_xml(user, uid)

    xsd_doc=etree.fromstring(USER_XSD.encode())

    xsd_schema = etree.XMLSchema(xsd_doc)
    xml_doc=etree.fromstring(user_xml_str)

    is_valid = xsd_schema.validate(xml_doc)

    if is_valid:
        
        # Get payload to update the newly created user in the ui
        payload=functions.get_payload_to_update_user(user,uid)
        logger.info(payload)
        logger.info(user_xml_str)
        # Updates user in the database
        API_calls.update_user(payload,user["pk"])
        logger.info("XML ist valid")
        return user_xml_str
    else:
        logger.info("XML note valid")
    # payload=get_payload_to_update_user(name_array[0],name_array[1],user,uid)
    # API_calls.update_user(payload,user["pk"])
    # return user_xml_str
    

# Function that enables us to publish messages on the queue
def publish_to_queue(xml_data):
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(IP, 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()
    logger.info(xml_data)
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
def f_update_xml(updated_user):

    payload={}
    

    user_xml_str = xmls.update_user_xml(updated_user)
    
    payload["name"]=updated_user["name"]
    payload["email"]=updated_user["email"]
    payload["phone"]=updated_user["phone"]
    payload["contact"]=""
    payload["currency"]="EUR"
    payload=json.dumps(payload)

    xsd_doc=etree.fromstring(USER_XSD.encode())

    xsd_schema = etree.XMLSchema(xsd_doc)
    xml_doc=etree.fromstring(user_xml_str)

    

    if xsd_schema.validate(xml_doc):     
        # Updates user in the database
        API_calls.update_user(payload,updated_user['pk'])
        logger.info("XML is valid")
        return user_xml_str
    else:
        logger.info("XML not valid")
    # API_calls.update_user(payload,updated_user['pk'])
    # return user_xml_str


# Function that checks the changes
def handle_user_update(updated_user):
    
    # Calls function to create the update XML
    update_xml = f_update_xml(updated_user)

    # Publish the updated user to the queue
    publish_to_queue(update_xml)
    
 
# Function that creates the XML to delete a user and returns it
def f_delete_xml(user_uid: str):

    user_xml_str = xmls.delete_user_xml(user_uid)

    xsd_doc=etree.fromstring(USER_XSD.encode())

    xsd_schema = etree.XMLSchema(xsd_doc)
    xml_doc=etree.fromstring(user_xml_str)


    if xsd_schema.validate(xml_doc):     
        # Updates user in the database
        logger.info("XML is valid")
        return user_xml_str
    else:
        logger.info("XML not valid")
    # return user_xml_str

#Handles the user delete
def handle_user_delete(deleted_user_uid: str):

    # Calls function to create an XML file
    delete_xml = f_delete_xml(deleted_user_uid)

    # Publishes the the deleted user to the queue
    publish_to_queue(delete_xml)
 
def main():
    
    # flag for if there was a change
    change=False

    while True:
        
        # Fetch updated users after 60 seconds
        time.sleep(20)

        # Fetches all the users in the database
        updated_users = functions.fetch_users()

        # Check for new users, updated users, and deleted users
        for updated_user in updated_users:
            if updated_user['description'] == "":
                change=True

                # New user detected
                user_xml = create_xml(updated_user)

                # Publishe the new user to the queue
                publish_to_queue(user_xml)

                # Adds the new user to the list

            elif updated_user['contact']=='update':

                # Get the old user json object


                # Handles the user to be updated
                handle_user_update(updated_user)





                change=True
            elif updated_user['contact']=='delete':
                


                handle_user_delete(updated_user['description'])

                uid= updated_user['description']
                # try:
                #     response=
                #     API_calls.log_to_controller_room('Deleting user', f"uid:{uid} has been deleted", False, datetime.datetime.now())
                # except:
                #     error_message = f"Error deleting user {uid}:"
                #     raise Exception(error_message)
                API_calls.delete_user(updated_user['pk'])

                API_calls.delete_user_pk_in_masterUuid(uid)
                # try:
                #     response= API_calls.delete_user_pk_in_masterUuid(uid)
                #     if response.status_code != 200:
                #         error_message = f"Error deleting user {uid} - Status code was not 204: {response.text}| status_code: {response.status_code}"
                #         raise Exception(error_message)
                #     else:
                #         API_calls.log_to_controller_room('Deleting user', f"uid:{uid} has been deleted", False, datetime.datetime.now())
                    
                # except Exception as e:
                #     error_message = f"Error accessing user {uid}: {str(e)}"
                #     raise Exception(error_message)

                




            
        if change==False:
            print("Nothing new")
        
 
 
if __name__ == "__main__":
    main()


