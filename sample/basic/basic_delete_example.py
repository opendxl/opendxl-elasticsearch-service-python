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

    # Create the delete request
    request_topic = "{}/delete".format(ELASTICSEARCH_API_TOPIC)
    req = Request(request_topic)

    # Set the payload for the delete request
    MessageUtils.dict_to_json_payload(req, {
        "index": DOCUMENT_INDEX,
        "doc_type": DOCUMENT_TYPE,
        "id": DOCUMENT_ID})

    # Send the delete request
    res = client.sync_request(req, timeout=30)

    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        # Display results for the index request
        res_dict = MessageUtils.json_payload_to_dict(res)
        print("Response to the delete request:\n{}".format(
            MessageUtils.dict_to_json(res_dict, pretty_print=True)))
    else:
        print("Error invoking service with topic '{}': {} ({})".format(
            request_topic, res.error_message, res.error_code))
        if res.payload:
            # Display the payload in the error response
            res_dict = MessageUtils.json_payload_to_dict(res)
            print("Error payload:\n{}".format(
                MessageUtils.dict_to_json(res_dict, pretty_print=True)))
