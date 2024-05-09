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
<order>
  <id>1</id>
  <user_id>123</user_id>
  <company_id>456</company_id>
  <products>
    <product>
      <id>1</id>
      <name>Coca Cola</name>
      <price>2.50</price>
      <amount>5</amount>
      <category>Soft drinks</category>
      <total>7.5</total>
      <totalExBtw>6.19</totalExBtw>
      <btw></btw>
    </product>
  </products>
  <total_price>260.00</total_price>
  <status>paid</status>
</order>
"""

# Publish the message to the exchange with routing key 'order.kassa'
channel.basic_publish(exchange=exchange_name, routing_key='order.kassa', body=order_xml)

print(" [x] Sent test order message")
# print(order_xml) #onnodig
# Close the connection
connection.close()