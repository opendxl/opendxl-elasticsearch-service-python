import os
import sys

from dxlbootstrap.util import MessageUtils
from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlclient.message import Request, Message

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

DOCUMENT_INDEX = "opendxl-elasticsearch-service-examples"
DOCUMENT_TYPE = "basic-example-doc"
DOCUMENT_ID = "12345"
ELASTICSEARCH_API_TOPIC = "/opendxl-elasticsearch/service/elasticsearch-api"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    # Create the update request
    request_topic = "{}/update".format(ELASTICSEARCH_API_TOPIC)
    update_request = Request(request_topic)

    # Set the payload for the update request
    MessageUtils.dict_to_json_payload(update_request, {
        "index": DOCUMENT_INDEX,
        "doc_type": DOCUMENT_TYPE,
        "id": DOCUMENT_ID,
        "body": {
            "doc": {
                "source": "Basic Update Example"}}})

    # Send the update request
    update_response = client.sync_request(update_request, timeout=30)

    if update_response.message_type != Message.MESSAGE_TYPE_ERROR:
        # Display results for the index request
        update_response_dict = MessageUtils.json_payload_to_dict(
            update_response)
        print("Response to the update request:\n{}".format(
            MessageUtils.dict_to_json(update_response_dict,
                                      pretty_print=True)))
    else:
        print("Error invoking service with topic '{}': {} ({})".format(
            request_topic, update_response.error_message,
            update_response.error_code))
        if update_response.payload:
            # Display the payload in the error response
            res_dict = MessageUtils.json_payload_to_dict(update_response)
            print("Error payload:\n{}".format(
                MessageUtils.dict_to_json(res_dict, pretty_print=True)))
        exit(1)

    # Create the get request
    request_topic = "{}/get".format(ELASTICSEARCH_API_TOPIC)
    get_request = Request(request_topic)

    # Set the payload for the get request
    MessageUtils.dict_to_json_payload(get_request, {
        "index": DOCUMENT_INDEX,
        "doc_type": DOCUMENT_TYPE,
        "id": DOCUMENT_ID})

    # Send the get request
    get_response = client.sync_request(get_request, timeout=30)

    if get_response.message_type != Message.MESSAGE_TYPE_ERROR:
        # Display results for the get request
        get_response_dict = MessageUtils.json_payload_to_dict(get_response)
        print("Response to the get request:\n{}".format(
            MessageUtils.dict_to_json(get_response_dict, pretty_print=True)))
    else:
        print("Error invoking service with topic '{}': {} ({})".format(
            request_topic, get_response.error_message,
            get_response.error_code))
