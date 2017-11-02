import json
import logging

from dxlbootstrap.util import MessageUtils

logger = logging.getLogger(__name__)


def on_event(event, index_operation):
    logger.info("Event payload received for transform: %s", event.payload)

    MessageUtils.decode_payload(event)
    index_operation["id"] = "advanced-event-example-id-1"
    index_operation["body"] = json.dumps({
        "id": index_operation["id"],
        "message": event.payload,
        "source": "Advanced Transform Example"})

    another_index_operation = {
        "index": index_operation["index"],
        "doc_type": index_operation["doc_type"],
        "id": "advanced-event-example-id-2",
        "body": json.dumps({
            "id": "advanced-event-example-id-2",
            "message": event.payload,
            "source": "Advanced Transform Example"})
    }

    return [index_operation, another_index_operation]
