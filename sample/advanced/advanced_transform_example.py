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
DOCUMENT_IDS = ["advanced-event-example-id-1", "advanced-event-example-id-2"]
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

    for document_id in DOCUMENT_IDS:
        # Create the get request
        request_topic = "{}/get".format(ELASTICSEARCH_API_TOPIC)
        req = Request(request_topic)

        # Set the payload for the get request
        MessageUtils.dict_to_json_payload(req, {
            "index": DOCUMENT_INDEX,
            "doc_type": DOCUMENT_TYPE,
            "id": document_id})

        tries_remaining = 5
        # Send up to 5 requests to the elasticsearch DXL service to try to
        # retrieve the document that should be stored for the event.
        res = client.sync_request(req, timeout=30)
        while res.message_type == Message.MESSAGE_TYPE_ERROR \
                and tries_remaining:
            tries_remaining -= 1
            time.sleep(2)
            res = client.sync_request(req, timeout=30)

        if res.message_type != Message.MESSAGE_TYPE_ERROR:
            # Display results for the get request
            res_dict = MessageUtils.json_payload_to_dict(res)
            print("Response to the get request for id '{}':\n{}".format(
                document_id,
                MessageUtils.dict_to_json(res_dict, pretty_print=True)))
        else:
            print("Error invoking service with topic '{}' for id '{}': {} ({})".format(
                request_topic, document_id, res.error_message, res.error_code))
            if res.payload:
                # Display the payload in the error response
                res_dict = MessageUtils.json_payload_to_dict(res)
                print("Error payload:\n{}".format(
                    MessageUtils.dict_to_json(res_dict, pretty_print=True)))
