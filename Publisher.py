import pika
import xml.etree.ElementTree as ET

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='order', exchange_type='direct')

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



def publish_order(ch, message):
    ch.basic_publish(exchange='order', routing_key='order.notify', body=message)
    print('[x] Sent order message')

xml_message = ET.Element('xml_message')
xml_message.text = order_xml

publish_order(channel, ET.tostring(xml_message, encoding='unicode'))

connection.close()
