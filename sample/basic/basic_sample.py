import os
import sys

from elasticsearch import Elasticsearch

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlclient.message import Message, Event, Request
from dxlbootstrap.util import MessageUtils

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

EVENT_TOPIC = "/eventstore/event"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    es_client = Elasticsearch([{"host": "localhost",
                                "port": 9200}])

    json_event_payload = { "hello" : "world",
                           "fruit": [ "orange", "apple"],
                           "testing" : True }

    json_event = Event(EVENT_TOPIC, json)
    client.send_event()
