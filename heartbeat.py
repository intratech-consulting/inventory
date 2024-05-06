import threading
import time
from datetime import datetime
import pika
import logging
import sys
import os
import requests
import HealthManager.py
from lxml import etree


manager = HealthManager()

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('heartbeat.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def send_heartbeat():

    logger = setup_logging()
    #connection = connect_to_rabbit()
    #channel = connection.channel()

    

    # Declare the queue and exchange, and make sure they are bound
    queue_name = 'heartbeat'
    exchange_name = 'heartbeat'
    routing_key = 'heartbeat'

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='heartbeat', durable=True)
    channel.exchange_declare(exchange='heartbeat', exchange_type='direct', durable=True)

    # Confirm that RabbitMQ will confirm messages
    channel.confirm_delivery()


    try:
        while True:
            if(manager.get_health==True):
                timestamp = datetime.now()
                heartbeat_xml = f"""
                <Heartbeat>
                    <Timestamp>{timestamp.isoformat()}</Timestamp>
                    <Status>Active</Status>
                    <SystemName>SystemNameHere</SystemName>
                </Heartbeat>
                """
                xml_doc = etree.fromstring(heartbeat_xml.encode())
                xsd_doc = etree.fromstring("""
                <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                    <xs:element name="Heartbeat">
                        <xs:complexType>
                            <xs:sequence>
                                <xs:element name="Timestamp" type="xs:dateTime" />
                                <xs:element name="Status" type="xs:string" />
                                <xs:element name="SystemName" type="xs:string" />
                            </xs:sequence>
                        </xs:complexType>
                    </xs:element>
                </xs:schema>
                """.encode())
                schema = etree.XMLSchema(xsd_doc)
                if schema.validate(xml_doc):
                    logger.info('XML is valid')
                    if channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=heartbeat_xml,
                                            mandatory=True):
                        logger.info('Message sent and confirmed')
                    else:
                        logger.error('Message sent but not confirmed')
                else:
                    logger.error('XML is not valid')
                time.sleep(2)
            else:
                time.sleep(interval)
    except pika.exceptions.UnroutableError:
        logger.error("Message was unroutable")
    finally:
        connection.close()

def receive_messages():
    # channel receiver cause using the same one create an error
    credentials = pika.PlainCredentials('guest', 'guest')  # Placeholder for credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='heartbeat', durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
    channel.basic_consume(queue='heartbeat', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def health_check_thread(url,interval):
    # healthcheck thread
    health_check_thread = threading.Thread(target=periodic_health_check, args=(url, interval))
    # will now exit when the main exits
    health_check_thread.daemon = True
    # Start the health check thread
    health_check_thread.start()
    print(f"Health check thread started for {url}. Checking every {interval} seconds.")
    
    # function that performs healthcheck
    def check_health(url):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic bHVjYXM6cm9vdA==',
                'Cookie': 'csrftoken=V2WgldExQx0XKqBh7VaEjKQAVdwv4HV2; sessionid=viptlrlxu6uqvfsmdebrqyh0f1n4kvk2'
            }
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                print(f"Connection to {url} is established.")
                manager.set_health=True
            else:
                print(f"Connection to {url} returned status code {response.status_code}.")
                manager.set_health=False
        except Exception as e:
            print(f"Connection to {url} failed: {e}")
            manager.set_health=False
    
    # performs healthcheck every x-amount of time
    def periodic_health_check(url, interval):
        while True:
            check_health(url)
            time.sleep(interval)
    
        


def main():
    logger = setup_logging()
    sender_thread = threading.Thread(target=send_heartbeat)
    receiver_thread = threading.Thread(target=receive_messages)
    sender_thread.start()
    receiver_thread.start()

    url = 'https://www.kfdemoedigevrienden.be/'
    # url='inventree.localhost/api/stock/#'
    interval = 5
    health_check_thread(url, interval)

    sender_thread.join()
    receiver_thread.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


 
if __name__ == "__main__":
    url = 'https://www.kfdemoedigevrenden.be/'
    interval = 5
    health_check_thread(url, interval)
   
    try:
        while True:
            time.sleep(1)
            print('true')
        else:
            print('false')
    except KeyboardInterrupt:
        print("Exiting...")