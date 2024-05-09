import pika
import xml.etree.ElementTree as ET

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Define the XML message payload
order_xml = """
<user__c>
    <user_id__c>1</user_id__c>
    <first_name__c>James</first_name__c>
    <last_name__c>Bond</last_name__c>
    <email__c>James.Bond007@hotmail.uk</email__c>
    <telephone__c>911</telephone__c>
    <birthday__c>11/11/1956</birthday__c>
    <country__c>United Kingdom</country__c>
    <state__c>null</state__c>
    <city__c>London</city__c>
    <zip__c>null</zip__c>
    <street__c>null</street__c>
    <house_number__c>null</house_number__c>
    <company_email__c>MI6@hotmail.uk/company_email__c>
    <company_id__c>5</company_id__c>
    <source__c>null</source__c>
    <user_role__c>null</user_role__c>
    <invoice__c>null</invoice__c>
    <calendar_link__c>null</calendar_link__c>
</user__c>
"""

# Publish the message to the exchange with routing key 'user.crm'
channel.basic_publish(exchange=exchange_name, routing_key='inventree.user.test', body=order_xml)

print(" [x] Sent test order message")
# print(order_xml) #onnodig
# Close the connection
connection.close()