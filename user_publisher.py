import time
import xml.etree.ElementTree as ET
import pika
import lxml
from lxml import etree
import json
import logging
from utilities import API_calls  # Import API calls module
from utilities import functions  # Import functions module

IP='10.2.160.51'

user_xsd="""
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="user">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="routing_key">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:minLength value="1"/>
                        </xs:restriction>
                    </xs:simpleType>
                </xs:element>
                <xs:element name="crud_operation">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:enumeration value="create"/>
                            <xs:enumeration value="update"/>
                            <xs:enumeration value="delete"/>
                        </xs:restriction>
                    </xs:simpleType>
                </xs:element>
                <xs:element name="id">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:minLength value="1"/>
                        </xs:restriction>
                    </xs:simpleType>
                </xs:element>
                <xs:element name="first_name" type="xs:string" nillable="true"/>
                <xs:element name="last_name" type="xs:string" nillable="true"/>
                <xs:element name="email" type="xs:string" nillable="true"/>
                <xs:element name="telephone" type="xs:string" nillable="true"/>
                <xs:element name="birthday">
                    <xs:simpleType>
                        <xs:union>
                            <xs:simpleType>
                                <xs:restriction base='xs:string'>
                                    <xs:length value="0"/>
                                </xs:restriction>
                            </xs:simpleType>
                            <xs:simpleType>
                                <xs:restriction base='xs:date' />
                            </xs:simpleType>
                        </xs:union>
                    </xs:simpleType>
                </xs:element>
                <xs:element name="address">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="country" type="xs:string" nillable="true"/>
                            <xs:element name="state" type="xs:string" nillable="true"/>
                            <xs:element name="city" type="xs:string" nillable="true"/>
                            <xs:element name="zip">
                                <xs:simpleType>
                                    <xs:union>
                                        <xs:simpleType>
                                            <xs:restriction base='xs:string'>
                                                <xs:length value="0"/>
                                            </xs:restriction>
                                        </xs:simpleType>
                                        <xs:simpleType>
                                            <xs:restriction base='xs:integer' />
                                        </xs:simpleType>
                                    </xs:union>
                                </xs:simpleType>
                            </xs:element>
                            <xs:element name="street" type="xs:string" nillable="true"/>
                            <xs:element name="house_number">
                                <xs:simpleType>
                                    <xs:union>
                                        <xs:simpleType>
                                            <xs:restriction base='xs:string'>
                                                <xs:length value="0"/>
                                            </xs:restriction>
                                        </xs:simpleType>
                                        <xs:simpleType>
                                            <xs:restriction base='xs:integer' />
                                        </xs:simpleType>
                                    </xs:union>
                                </xs:simpleType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="company_email" type="xs:string" nillable="true"/>
                <xs:element name="company_id" type="xs:string" nillable="true"/>
                <xs:element name="source" type="xs:string"  nillable="true"/>
                <xs:element name="user_role">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:enumeration value="speaker"/>
                            <xs:enumeration value="individual"/>
                            <xs:enumeration value="employee"/>
                            <xs:enumeration value=""/>
                        </xs:restriction>
                    </xs:simpleType>
                </xs:element>
                <xs:element name="invoice" type="xs:string" nillable="true"/>
                <xs:element name="calendar_link" type="xs:string" nillable="true"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
"""

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
    ET.SubElement(user_element, "telephone").text = user['phone']
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

    user_xml_str = ET.tostring(user_element, encoding='unicode')



    # xsd_doc=etree.fromstring(user_xsd.encode())

    # xsd_schema = etree.XMLSchema(xsd_doc)
    # xml_doc=etree.fromstring(user_xml_str)

    # is_valid = xsd_schema.validate(xml_doc)

    # if is_valid:
        
    #     # Get payload to update the newly created user in the ui
    #     payload=get_payload_to_update_user(name_array[0],name_array[1],user,uid)
    #     logger.info(payload)
    #     logger.info(user_xml_str)
    #     # Updates user in the database
    #     API_calls.update_user(payload,user["pk"])
    #     logger.info("XML ist valid")
    #     return user_xml_str
    # else:
    #     logger.info("XML note valid")
    payload=get_payload_to_update_user(name_array[0],name_array[1],user,uid)
    API_calls.update_user(payload,user["pk"])
    return user_xml_str
    

    

    

    
    

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
def f_update_xml(updated_user, updated_fields):
    payload={}
    user_element = ET.Element("user")
    ET.SubElement(user_element, "routing_key").text = "user.inventory"
    ET.SubElement(user_element, "crud_operation").text = "update"
    ET.SubElement(user_element, "id").text = updated_user['description']
    ET.SubElement(user_element, "first_name").text = updated_fields["first_name"]
    ET.SubElement(user_element, "last_name").text = updated_fields["last_name"]
    ET.SubElement(user_element, "telephone").text = updated_fields['telephone']
    ET.SubElement(user_element, "email").text = updated_fields['email']
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

    user_xml_str = ET.tostring(user_element, encoding='unicode')
    
    payload["name"]=updated_user["name"]
    payload["email"]=updated_user["email"]
    payload["phone"]=updated_user["phone"]
    payload["contact"]=""
    payload["currency"]="EUR"
    payload=json.dumps(payload)

    # xsd_doc=etree.fromstring(user_xsd.encode())

    # xsd_schema = etree.XMLSchema(xsd_doc)
    # xml_doc=etree.fromstring(user_xml_str)

    # is_valid = xsd_schema.validate(xml_doc)

    # if is_valid:     
    #     # Updates user in the database
    #     API_calls.update_user(payload,updated_user['pk'])
    #     logger.info("XML is valid")
    #     return user_xml_str
    # else:
    #     logger.info("XML not valid")
    API_calls.update_user(payload,updated_user['pk'])
    return user_xml_str


# Function that checks the changes
def handle_user_update(updated_user):

    #Empty array to be filled
    updated_fields = {}

    # Extract first name and last name from the company_name field
    updated_user_name_array=updated_user['name'].split('.')
    
    # Pasting the first & last names into variables
    updated_fields["first_name"] = updated_user_name_array[0]
    updated_fields["last_name"] =  updated_user_name_array[1]
    updated_fields["email"]=updated_user["email"]
    updated_fields["telephone"]=updated_user["phone"]
 

    # Calls function to create the update XML
    update_xml = f_update_xml(updated_user, updated_fields)

    # Publish the updated user to the queue
    publish_to_queue(update_xml)
    
 
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
    ET.SubElement(user_element, "telephone").text = None
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
    
    user_xml_str = ET.tostring(user_element, encoding='unicode')



    # xsd_doc=etree.fromstring(user_xsd.encode())

    # xsd_schema = etree.XMLSchema(xsd_doc)
    # xml_doc=etree.fromstring(user_xml_str)

    # is_valid = xsd_schema.validate(xml_doc)

    # if is_valid:     
    #     # Updates user in the database
    #     logger.info("XML is valid")
    #     return user_xml_str
    # else:
    #     logger.info("XML not valid")
    return user_xml_str

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

            elif updated_user['contact']=='update':

                # Get the old user json object


                # Handles the user to be updated
                handle_user_update(updated_user)





                change=True
            elif updated_user['contact']=='delete':


                handle_user_delete(updated_user['description'])

                API_calls.delete_user(updated_user['pk'])



                change=True
            
        if change==False:
            print("Nothing new")
        
 
 
if __name__ == "__main__":
    main()


