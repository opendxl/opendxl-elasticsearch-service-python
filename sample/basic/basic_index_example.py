import json
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

SERVICE_UNIQUE_ID = "test"

DOCUMENT_INDEX = "test_index"
DOCUMENT_TYPE = "test_doc"
DOCUMENT_ID = "12345"
ELASTICSEARCH_API_TOPIC = "/opendxl-elasticsearch/service/elasticsearch-api"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    # Create the index request
    request_topic = "{}/{}/index".format(
        ELASTICSEARCH_API_TOPIC, SERVICE_UNIQUE_ID)
    index_request = Request(request_topic)

    # Set the payload for the index request
    body_payload = json.dumps({
        "message": "Hello from OpenDXL",
        "source": "Basic Index Example"}).encode(encoding="utf-8")
    index_request.payload = json.dumps({
        "index": DOCUMENT_INDEX,
        "doc_type": DOCUMENT_TYPE,
        "id": DOCUMENT_ID,
        "body": body_payload}).encode(encoding="utf-8")

    # Send the index request
    index_response = client.sync_request(index_request, timeout=30)

    if index_response.message_type != Message.MESSAGE_TYPE_ERROR:
        # Display results for the index request
        index_response_dict = MessageUtils.json_payload_to_dict(index_response)
        print("Response to the index request:\n{}".format(
            MessageUtils.dict_to_json(index_response_dict, pretty_print=True)))
    else:
        print("Error invoking service with topic '{}': {} ({})".format(
            request_topic, index_response.error_message,
            index_response.error_code))
        exit(1)

    # Create the get request
    request_topic = "{}/{}/get".format(
        ELASTICSEARCH_API_TOPIC, SERVICE_UNIQUE_ID)
    get_request = Request(request_topic)

    # Set the payload for the get request
    get_request.payload = json.dumps({
        "index": DOCUMENT_INDEX,
        "doc_type": DOCUMENT_TYPE,
        "id": DOCUMENT_ID}).encode(encoding="utf-8")

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
