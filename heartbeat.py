from lxml import etree
import pika
import time
from datetime import datetime
import logging
import sys  # Import for system operations
import os   # Import for operating system operations

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

    # Common XML and XSD
    heartbeat_xsd = """
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
    """

    # RabbitMQ setup
    credentials = pika.PlainCredentials('change before testing', 'change before testing')  # Placeholder for credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', "change before testing 5672", '/', credentials))
    channel = connection.channel()

    queue_name = 'change before testing'  # Placeholder for queue name
    channel.queue_declare(queue="change before testing", durable=True)

    try:
        while True:
            timestamp = datetime.now()
            heartbeat_xml = f"""
            <Heartbeat>
                <Timestamp>{timestamp.isoformat()}</Timestamp>
                <Status>Active</Status>
                <SystemName>SystemNameHere</SystemName>  # Change "SystemNameHere" to actual system name
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

            channel.basic_publish(exchange='', routing_key=queue_name, body=heartbeat_xml)
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
