import datetime
import time
import pika
from lxml import etree
import docker  # Import Docker library

TEAM = 'inventory'  # Service name

# Define your XML and XSD as strings
heartbeat_xml = """
<Heartbeat>
    <Timestamp>{timestamp}</Timestamp>
    <Status>{status}</Status>
    <SystemName>{system_name}</SystemName>
    <ErrorLog>{error_log}</ErrorLog>
</Heartbeat>
"""

heartbeat_xsd = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="Heartbeat">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="Timestamp" type="xs:dateTime" />
                <xs:element name="Status" type="xs:string" />
                <xs:element name="SystemName" type="xs:string" />
                <xs:element name="ErrorLog" type="xs:string" />
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
"""

# Parse the documents
xsd_doc = etree.fromstring(heartbeat_xsd.encode())
schema = etree.XMLSchema(xsd_doc)

# Setup RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.53', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()
channel.queue_declare(queue='heartbeat_queue', durable=True)

# Setup Docker client
client = docker.from_env()

def is_container_running(container_name):
    """Check if the specified container is running and return status or error message."""
    try:
        container = client.containers.get(container_name)
        if container.status == 'running':
            return True, ""
        else:
            return False, f"Container status is {container.status}."
    except Exception as e:
        return False, f"Error getting container status: {e}"

container_name = 'inventree-db'  # Docker container name

# Loop to send heartbeat message
try:
    while True:
        running, error_log = is_container_running(container_name)
        if running:
            status = 'Active'
            error_log = ""  # Clear error log when container is running
        else:
            status = 'Inactive'
            print(f"{error_log}, retrying in 5 seconds.")
            time.sleep(5)  # Wait for 5 seconds before retrying
            continue  # Skip sending the message when container is down

        # Prepare XML with error log
        formatted_heartbeat_xml = heartbeat_xml.format(
            timestamp=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            status=status,
            system_name=TEAM,  # Use the TEAM variable for SystemName
            error_log=error_log
        )
        xml_doc = etree.fromstring(formatted_heartbeat_xml.encode())

        # Validate XML
        if schema.validate(xml_doc):
            print('XML is valid')
            channel.basic_publish(exchange='', routing_key='heartbeat_queue', body=formatted_heartbeat_xml)
            print('Message sent')
        else:
            print('XML is not valid')

        time.sleep(1)  # Wait for 1 second before sending another message
except KeyboardInterrupt:
    print("Script interrupted by user.")
finally:
    connection.close()
    print("Connection closed.")