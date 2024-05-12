import pika

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.53', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
routing_key = 'user.inventree'
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Define the updated XML message payload
payload = '''
<user>
    <routing_key>user.crm</routing_key>
    <crud_operation>delete</crud_operation>
    <id>5e2531a0-71cf-4540-a56b-475a8f31bb80</id>
    <first_name>Zico</first_name>
    <last_name>Doe</last_name>
    <email>12john.doe@mail.com</email>
    <telephone>+32467179912</telephone>
    <birthday>2024-04-14</birthday>
    <address>
        <country>Belgium</country>
        <state>Brussels</state>
        <city>Brussels</city>
        <zip>1000</zip>
        <street>Nijverheidskaai</street>
        <house_number>170</house_number>
    </address>
    <company_email>8john.doe@company.com</company_email>
    <company_id>a03Qy000004cOQUIA2</company_id>
    <source>salesforce</source>
    <user_role>speaker</user_role>
    <invoice>BE00 0000 0000 0000</invoice>
    <calendar_link>www.example.com</calendar_link>
</user>
'''

# Publish the message to the exchange with routing key 'user.crm'
channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=payload)

print(" [x] Sent test order message")
# Close the connection
connection.close()
