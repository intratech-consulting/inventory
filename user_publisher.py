import pika
import xml.etree.ElementTree as ET

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
routing_key='user.inventree'
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Define the XML message payload
payload = f'''

    <user>
    <routing_key>{routing_key}</routing_key>
    <user_id>007</user_id>
    <first_name>James</first_name>
    <last_name>Bond</last_name>
    <email>James.Bond@mail.com</email>
    <telephone>+32467179912</telephone>
    <birthday>2024-04-14</birthday>
    <address>
            <country>United Kindom</country>
            <state>Londen</state>
            <city>Londen</city>
            <zip>1000</zip>
            <street>Nijverheidskaai</street>
            <house_number>007</house_number>
    </address>
    <company_email>john.doe@company.com</company_email>
    <company_id>a03Qy000004cOQUIA2</company_id>
    <source>salesforce</source>
    <user_role>Employee</user_role>
    <invoice>Yes</invoice>
    <calendar_link>www.example.com</calendar_link>
</user>

    '''

# Publish the message to the exchange with routing key 'user.crm'
channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=payload)

print(" [x] Sent test order message")
# print(order_xml) #onnodig
# Close the connection
connection.close()