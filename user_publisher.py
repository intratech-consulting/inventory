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

        <routing_key>{routing_key}<routing_key>

        <first_name>James</first_name>

        <last_name>Bond</last_name>

        <email>James.Bond@hotmail.com</email>

        <telephone>911</telephone>

        <birthday>6</birthday>

        <address>
        
            <country>United Kingdom</country>

            <state>8</state>

            <city>9</city>

            <zip>10</zip>

            <street>11</street>

        </address>

        <house_number>7</house_number>

        <company_email></company_email>

        <company_id>14</company_id>

        <source>15</source>

        <user_role>Speaker</user_role>

        <invoice>17</invoice>

        <calendar_link>18</calendar_link>

    </user>

    '''

# Publish the message to the exchange with routing key 'user.crm'
channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=payload)

print(" [x] Sent test order message")
# print(order_xml) #onnodig
# Close the connection
connection.close()