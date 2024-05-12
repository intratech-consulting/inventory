import pika

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.53', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Define the updated XML message payload
order_xml = """
<order>
    <routing_key>order.crm</routing_key>
    <crud_operation>create</crud_operation>
    <id>123</id>
    <user_id>0123</user_id>
    <company_id>3210</company_id>
    <products>
        <product>
            <product_id>1</product_id>
            <name>Coca Cola</name>
            <amount>5</amount>
        </product>
    </products>
    <total_price>260.00</total_price>
    <status>paid</status>
</order>
"""

# Publish the message to the exchange with routing key 'order.kassa'
channel.basic_publish(exchange=exchange_name, routing_key='order.kassa', body=order_xml)

print(" [x] Sent test order message")
# Close the connection
connection.close()
