import json
from . import API_calls
import requests

def payload_extracting_update_user(user_xml,user_pk):
    try:
        first_name = user_xml.find('first_name').text
    except:
        first_name=None

    try:
        last_name = user_xml.find('last_name').text
    except:
        last_name=None

    try:
        phone = user_xml.find('telephone').text
    except:
        phone=None

    try:
        email = user_xml.find('email').text
    except:
        email=None

    if email is None and phone is None and last_name is None and first_name is None:
        raise Exception("relevant fields were empty")
    return payload_update_user(user_pk,first_name, last_name, phone, email)

def payload_update_user(user_pk,first_name=None, last_name=None, telephone=None, email=None):
    # Create an empty payload dictionary
    payload = {}

    # Bool to flag if
    empty=False
    # Get the name from the user because it's required
    request=API_calls.get_user(user_pk)
    data=request.json()
    name=data['name']
    name_array=name.split(".")

    # Add name to payload because it's required
    if first_name is None and last_name is None:
        
        payload["name"] = name
    # Add name field if both first_name and last_name are provided
    if first_name is not None and last_name is None:
        last_name=name_array[1]
        payload["name"] = f"{first_name}.{last_name}"

    if first_name is None and last_name is not None:
        first_name=name_array[0]
        payload["name"] = f"{first_name}.{last_name}"

    if first_name is not None and last_name is not None:
        payload["name"] = f"{first_name}.{last_name}"

    # Add phone field if telephone is provided
    if telephone is not None:
        payload["phone"] = telephone

    # Add email field if email is provided
    if email is not None:
        payload["email"] = email

    #currency is mandatory
    payload["currency"]="EUR"

    # Convert payload dictionary to JSON string
    return json.dumps(payload)

        
def get_user_with_same_uid(uid,list):
    data=list
    for user in data:
        if user['description']==uid:
            return user
    return False
        
def find_user_in_list(list,old_user):
    for new_user in list:
        if new_user['description']==old_user['description']:
            return False
    return True
  
def compare_json_objects(updated_user, user_list):
    old_user=get_user_with_same_uid(updated_user['description'], user_list)
    if old_user==False:
        user_list.append(updated_user)
        return False

    # obj1 = json.loads(str(updated_user))
    # obj2 = json.loads(old_user)
    
    # Compare the dictionaries
    if updated_user==old_user:
        return False
    else:
        return True
    
# Function to that makes a payload to update the user without a description(user made in the ui)
def get_payload_to_update_user(user,uid):
    user_name=user['name']

    payload = json.dumps(
            {
                "name": user_name,
                "description": uid,
                "currency": "EUR",
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False,
            }
        )
    return payload

# Function that returns the list of users in inventree
def fetch_users():
    response = API_calls.get_users()
    users = response.json()
    print(f"fetching is done")
    return users

def uid_checker(user):
    try:
        is_invalid_uid = API_calls.masterUuid_check(user['description'])
        
        if is_invalid_uid:
            uid = API_calls.get_uid_from_pk(f"u.{user['pk']}")
            payload = json.dumps(
            {
                "name": user['name'],
                "description": uid,
                "currency": "EUR",
                "contact":"ERROR: uid was incorrect, is now recovered but nothing was published.",
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False
            }
            )
            response = API_calls.update_user(payload, user['pk'])
            raise Exception(f"uid was altered, is now reset")
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 404:
            uid = API_calls.get_uid_from_pk(f"u.{user['pk']}")

            payload = json.dumps(
            {
                "name": user['name'],
                "description": uid,
                "currency": "EUR",
                "contact":"ERROR: uid was incorrect, is now recovered but nothing was published.",
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False
            }
            )
            response = API_calls.update_user(payload, user['pk'])
            raise Exception(f"uid was altered, is now reset")
        else:
            raise Exception(f"Something went wrong when checking the uid: {str(e)}")
