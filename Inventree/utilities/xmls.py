import xml.etree.ElementTree as ET
import lxml
from lxml import etree
from . import API_calls
import json





def create_user_xml(user,uid):
    try:
        name = user['name']
        name_array = name.split(".")
        # Probeer toegang te krijgen tot het eerste element in name_array
        first_element = name_array[0]
        print(f"First element: {first_element}")
    except IndexError:
        payload = json.dumps(
            {
                "name": "ERROR",
                "currency": "EUR",
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False,
                "notes":"first & last name must be seperated with '.'"
            }
            )
        error_message="XML not valid, created user has not been published, uid has been deleted, name had no '.'"
        API_calls.delete_user_pk_in_masterUuid(uid)
        API_calls.update_user(payload, user['pk'])
        raise Exception(error_message)
    except Exception as e:
        error_message=f"XML not valid, created user has not been published, uid has been deleted : {str(e)}"
        API_calls.delete_user_pk_in_masterUuid(uid)
        raise Exception(error_message)
    
    user_element = ET.Element("user")
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

    return ET.tostring(user_element, encoding='unicode')

def update_user_xml(user):
    try:
        name = user['name']
        name_array = name.split(".")
        # Probeer toegang te krijgen tot het eerste element in name_array
        first_element = name_array[0]
        print(f"First element: {first_element}")
    except IndexError:
        payload = json.dumps(
            {
                "name": "ERROR",
                "currency": "EUR",
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False,
                "notes":"first & last name must be seperated with '.'"
            }
            )
        error_message="XML not valid, updated user has not been published, name has no '.'"
        API_calls.update_user(payload, user['pk'])
        raise Exception(error_message)
    except Exception as e:
        error_message=f"XML not valid, updated user has not been published : {str(e)}"
        raise Exception(error_message)
    
    
    user_element = ET.Element("user")
    ET.SubElement(user_element, "routing_key").text = 'user.inventory'
    ET.SubElement(user_element, "crud_operation").text = 'update'
    ET.SubElement(user_element, "id").text = user['description']
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

    return ET.tostring(user_element, encoding='unicode')

def delete_user_xml(uid):

    # Creating the body
    user_element = ET.Element("user")
    ET.SubElement(user_element, "routing_key").text = "user.inventory"
    ET.SubElement(user_element, "crud_operation").text = "delete"
    ET.SubElement(user_element, "id").text = uid

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

    return ET.tostring(user_element, encoding='unicode')