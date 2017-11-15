import os
import sys
import time

from dxlbootstrap.util import MessageUtils
from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlclient.message import Event, Request, Message

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

DOCUMENT_INDEX = "opendxl-elasticsearch-service-examples"
DOCUMENT_TYPE = "advanced-transform-example-doc"
FIRST_DOCUMENT_ID = "advanced-event-example-id-1"
SECOND_DOCUMENT_ID = "advanced-event-example-id-2"
EVENT_TOPIC = "/sample/elasticsearch/advancedtransform"
ELASTICSEARCH_API_TOPIC = "/opendxl-elasticsearch/service/elasticsearch-api"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    # Create the event
    event = Event(EVENT_TOPIC)

    # Set the payload
    MessageUtils.encode_payload(event, "Hello from OpenDXL")

    # Send the event
    client.send_event(event)

    print("Waiting for event payloads to be stored in Elasticsearch...")
    time.sleep(5)

    # Create a get request
    request_topic = "{}/get".format(ELASTICSEARCH_API_TOPIC)
    req = Request(request_topic)

    # Set the payload for the get request for the first document
    MessageUtils.dict_to_json_payload(req, {
        "index": DOCUMENT_INDEX,
        "doc_type": DOCUMENT_TYPE,
        "id": FIRST_DOCUMENT_ID})

    # Send a request to the elasticsearch DXL service to retrieve the first
    # document that should be stored for the event.
    res = client.sync_request(req, timeout=30)

    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        # Display results for the get request for the first document
        res_dict = MessageUtils.json_payload_to_dict(res)
        print("Response to the get request for id '{}':\n{}".format(
            FIRST_DOCUMENT_ID,
            MessageUtils.dict_to_json(res_dict, pretty_print=True)))
    else:
        print("Error invoking service with topic '{}' for id '{}': {} ({})".format(
            request_topic, FIRST_DOCUMENT_ID, res.error_message, res.error_code))
        if res.payload:
            # Display the payload in the error response
            res_dict = MessageUtils.json_payload_to_dict(res)
            print("Error payload:\n{}".format(
                MessageUtils.dict_to_json(res_dict, pretty_print=True)))

    # Set the payload for the get request for the second document
    MessageUtils.dict_to_json_payload(req, {
        "index": DOCUMENT_INDEX,
        "doc_type": DOCUMENT_TYPE,
        "id": SECOND_DOCUMENT_ID})

    # Send a request to the elasticsearch DXL service to retrieve the second
    # document that should be stored for the event.
    res = client.sync_request(req, timeout=30)

    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        # Display results for the get request for the second document
        res_dict = MessageUtils.json_payload_to_dict(res)
        print("Response to the get request for id '{}':\n{}".format(
            SECOND_DOCUMENT_ID,
            MessageUtils.dict_to_json(res_dict, pretty_print=True)))
    else:
        print("Error invoking service with topic '{}' for id '{}': {} ({})".format(
            request_topic, SECOND_DOCUMENT_ID, res.error_message, res.error_code))
        if res.payload:
            # Display the payload in the error response
            res_dict = MessageUtils.json_payload_to_dict(res)
            print("Error payload:\n{}".format(
                MessageUtils.dict_to_json(res_dict, pretty_print=True)))
