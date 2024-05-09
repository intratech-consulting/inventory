import pika
import xml.etree.ElementTree as ET

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Define the XML message payload
payload = f'''

    <user__c>

        <first_name__c>James</first_name__c>

        <last_name__c>Bond</last_name__c>

        <email__c>James.Bond@hotmail.com</email__c>

        <telephone__c>911</telephone__c>

        <birthday__c>6</birthday__c>

        <country__c>7</country__c>

        <state__c>8</state__c>

        <city__c>9</city__c>

        <zip__c>10</zip__c>

        <street__c>11</street__c>

        <house_number__c>12</house_number__c>

        <company_email__c>13</company_email__c>

        <company_id__c>14</company_id__c>

        <source__c>15</source__c>

        <user_role__c>16</user_role__c>

        <invoice__c>17</invoice__c>

        <calendar_link__c>18</calendar_link__c>

    </user__c>

    '''

# Publish the message to the exchange with routing key 'user.crm'
channel.basic_publish(exchange=exchange_name, routing_key='user.inventree', body=payload)

print(" [x] Sent test order message")
# print(order_xml) #onnodig
# Close the connection
connection.close()