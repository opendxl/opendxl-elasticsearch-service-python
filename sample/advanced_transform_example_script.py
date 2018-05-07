from __future__ import absolute_import
import logging

from dxlbootstrap.util import MessageUtils

logger = logging.getLogger(__name__)


def on_event(event, index_operation):
    """
    Callback invoked with content received for a DXL event. The callback should
    return a dictionary (or list of dictionaries) with parameters for the
    Elasticsearch index operation(s) that the service should perform.

    The elements for each dictionary returned should correspond to parameters
    in the `Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`__.
    For example, the value for the "doc_type" element in the dictionary will be
    supplied as the "doc_type" parameter for the Elasticsearch "index"
    operation.

    :param dxlclient.message.Event event: The event which was received.
    :param dict index_operation: A dict with a set of parameters configured
        for storing the event payload into Elasticsearch. The dictionary
        should include the following:

        .. code-block::python

            { "index": "<documentIndex value from the application config>",
              "doc_type": "<documentType value from the application config>",
              "body": "<payload from the event parameter>",
              "id": "<id from event payload>" }

        If the event payload could be converted into a dict from JSON, the
        value for the "body" element will be a dict. Otherwise, the payload
        will be a str.

        The value for the "id" element is pulled from the value for the key
        in the event payload which corresponds to the "idFieldName" value
        in the application configuration. If no value was set for "idFieldName"
        in the application configuration, the value for the "id" element is
        None.

    :return: A dictionary (or list of dictionaries) with parameters for an
        Elasticsearch "index" operation to perform. If None is returned, no
        "index" operations will be performed.
    :rtype: dict or list(dict)
    """
    logger.info("Event payload received for transform: %s", event.payload)
    logger.info("Index operation received for transform: %s", index_operation)

    # Modify the "id" and "body" elements in the index operation dictionary.
    event_payload = MessageUtils.decode_payload(event)
    index_operation["id"] = "advanced-event-example-id-1"
    # Store the event payload string in a dictionary. This allows Elasticsearch
    # to serialize the document into JSON for storage.
    index_operation["body"] = MessageUtils.dict_to_json({
        "id": index_operation["id"],
        "message": event_payload,
        "source": "Advanced Transform Example"})

    # Create a second index operation dictionary, using some of the values
    # from the first dictionary.
    another_index_operation = {
        "index": index_operation["index"],
        "doc_type": index_operation["doc_type"],
        "id": "advanced-event-example-id-2",
        "body": MessageUtils.dict_to_json({
            "id": "advanced-event-example-id-2",
            "message": event_payload,
            "source": "Advanced Transform Example"})
    }

    # Return info for two documents to store in Elasticsearch.
    return [index_operation, another_index_operation]
