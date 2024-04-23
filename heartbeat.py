from lxml import etree
import pika
import time
from datetime import datetime
import logging
import sys
import os

def setup_logging():
    # Setup basic logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler
    handler = logging.FileHandler('heartbeat.log')
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)
    return logger


def main():
    logger = setup_logging()
    try:
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    except pika.exceptions.AMQPConnectionError as e:
        logger.error("Failed to connect to RabbitMQ", exc_info=True)
        return  # Exit if connection failed

    # Common XML and XSD
    heartbeat_xsd = """
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <xs:element name="Heartbeat">
            <xs:complexType>
                <xs:sequence>
                    <xs:element name="id" type="xs:integer" />
                    <xs:element name="name" type="xs:string" />
                    <xs:element name="category" type="xs:string" />
                    <xs:element name="amount" type="xs:integer" />
                    <xs:element name="location" type="xs:string" />
                    <xs:element name="amount_in_stock" type="xs:integer" />
                </xs:sequence>
            </xs:complexType>
        </xs:element>
    </xs:schema>
    """

    # RabbitMQ setup
    credentials = pika.PlainCredentials('guest', 'guest')  # Placeholder for credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    #when running application in a docker network with rabbit mq host must be name of container
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))

    channel = connection.channel()

    queue_name = 'heartbeat'  # Placeholder for queue name
    channel.queue_declare(queue=f"{queue_name}", durable=True)
    channel.exchange_declare(exchange='heartbeat', exchange_type='direct', durable=True)

    try:
        while True:
            timestamp = datetime.now()
            # heartbeat_xml = f"""
            # <Heartbeat>
            #     <id>1</id>
            #     <name>coca cola</name>
            #     <category>softdrink</category>
            #     <amount>2</amount>
            # </Heartbeat>
            # """
            heartbeat_xml = f"""
            <Heartbeat>
                <id>1</id>
                <name>coca cola</name>
                <category>softdrink</category>
                <amount>2</amount>
                <location>A1</location>
                <amount_in_stock>20</amount_in_stock>
            </Heartbeat>
            """


            # Parsing and validation
            xml_doc = etree.fromstring(heartbeat_xml.encode())
            xsd_doc = etree.fromstring(heartbeat_xsd.encode())
            schema = etree.XMLSchema(xsd_doc)
            if schema.validate(xml_doc):
                logger.info('XML is valid')
            else:
                logger.error('XML is not valid')

            channel.basic_publish(exchange='heartbeat', routing_key=queue_name, body=heartbeat_xml)
            logger.info('Message sent')
            time.sleep(2)  # Send message every 2 seconds
    except KeyboardInterrupt:
        logger.info("Stopping gracefully...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        connection.close()
        logger.info("Connection closed")


if __name__ == '__main__':
    main()