import json
from . import API_calls

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

        
    