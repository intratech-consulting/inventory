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

#constants
IP=constants.IP
USER_XSD_U_D=xsds.get_user_update_and_delete_xsd()
USER_XSD_C=xsds.get_user_create_xsd()


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

    xsd_doc=etree.fromstring(USER_XSD_C.encode())

    xsd_schema = etree.XMLSchema(xsd_doc)
    xml_doc=etree.fromstring(user_xml_str)

    is_valid = xsd_schema.validate(xml_doc)

    if is_valid:
        
        # Get payload to update the newly created user in the ui
        payload=functions.get_payload_to_update_user(user,uid)
        logger.info(payload)
        # Updates user in the database
        API_calls.update_user(payload,user["pk"])
        return user_xml_str
    else:
        error_message="XML not valid"
        raise Exception(error_message)
    

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

    # Payload for inventree
    payload={}
    

    user_xml_str = xmls.update_user_xml(updated_user)
    
    payload["name"]=updated_user["name"]
    payload["email"]=updated_user["email"]
    payload["phone"]=updated_user["phone"]
    payload["contact"]=""
    payload["currency"]="EUR"
    payload=json.dumps(payload)

    xsd_doc=etree.fromstring(USER_XSD_U_D.encode())

    xsd_schema = etree.XMLSchema(xsd_doc)
    xml_doc=etree.fromstring(user_xml_str)

    
    # validates xml
    if xsd_schema.validate(xml_doc):     
        # Updates user in the database
        API_calls.update_user(payload,updated_user['pk'])
        return user_xml_str
    else:
        error_message="XML not valid"
        raise Exception(error_message)


# Function that checks the changes
def handle_user_update(updated_user):
    
    # Calls function to create the update XML
    update_xml = f_update_xml(updated_user)

    try:
        publish_to_queue(update_xml)
    except Exception as e:
        error_message=f"Error deleting user {updated_user['description']}: {str(e)}"
        raise Exception(error_message)
    # Publish the updated user to the queue
    
    
 
# Function that creates the XML to delete a user and returns it
def f_delete_xml(user_uid: str):

    user_xml_str = xmls.delete_user_xml(user_uid)

    xsd_doc=etree.fromstring(USER_XSD_U_D.encode())

    xsd_schema = etree.XMLSchema(xsd_doc)
    xml_doc=etree.fromstring(user_xml_str)

    # validates xml
    if xsd_schema.validate(xml_doc):     
        # Updates user in the database
        return user_xml_str
    else:
        error_message="XML not valid"
        raise Exception(error_message)
    
    # return user_xml_str

#Handles the user delete
def handle_user_delete(deleted_user_uid: str):

    # Calls function to create an XML file
    delete_xml = f_delete_xml(deleted_user_uid)

    # Publishes the the deleted user to the queue
    try:
        publish_to_queue(delete_xml)
    except Exception as e:
        error_message=f"Error deleting user {deleted_user_uid}: {str(e)}"
        raise Exception(error_message)
 
def main():
    
    # flag for if there was a change
    change=False

    while True:
        
        # Fetch updated users after 60 seconds
        time.sleep(20)

        # Fetches all the users in the database
        try:
            updated_users = functions.fetch_users()
        except:
            API_calls.log_to_controller_room('Error, publishing user', "failed to fetch users from db", True, datetime.datetime.now())

        # Check for new users, updated users, and deleted users
        for updated_user in updated_users:
            # Check for new user without description (uid)
            if updated_user['description'] == "":
                change=True

                # New user detected
                try:
                    
                    user_xml = create_xml(updated_user)
                    publish_to_queue(user_xml)
                    API_calls.log_to_controller_room('P_CREATE user ', "user succesfully created", False, datetime.datetime.now())
                except Exception as e:
                    error_message=f"Error processing message:\n{str(e)}"
                    API_calls.log_to_controller_room('ERROR P_CREATE user ', error_message, True, datetime.datetime.now())
            
            # Check for users need to be update by checking contact field for update
            elif updated_user['contact']=='update':
                try:
                    handle_user_update(updated_user)
                    API_calls.log_to_controller_room('P_UPDATE user ', "user succesfully updated", False, datetime.datetime.now())
                except:
                    error_message=f"Error processing message:\n{str(e)}"
                    API_calls.log_to_controller_room('ERROR P_UPDATE user', error_message, True, datetime.datetime.now())
                change=True

            # Check for user need to be deleted by checking contact field for delete
            elif updated_user['contact']=='delete':         
                try:
                    handle_user_delete(updated_user['description'])
                    uid= updated_user['description']
                    API_calls.delete_user(updated_user['pk'])
                    API_calls.delete_user_pk_in_masterUuid(uid)
                    API_calls.log_to_controller_room('P_DELETE user ', "user succesfully deleted", False, datetime.datetime.now())
                except:
                    error_message=f"Error processing message:\n{str(e)}"
                    API_calls.log_to_controller_room('ERROR P_DELETE user', error_message, True, datetime.datetime.now())   
        if change==False:
            print("Nothing new")
        
if __name__ == "__main__":
    main()


