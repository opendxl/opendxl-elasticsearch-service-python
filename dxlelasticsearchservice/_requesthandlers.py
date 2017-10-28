import logging

from elasticsearch import Elasticsearch

from dxlbootstrap.util import MessageUtils
from dxlclient.callbacks import EventCallback

# Configure local logger
logger = logging.getLogger(__name__)


class ElasticSearchServiceEventCallback(EventCallback):
    """
    """
    def __init__(self, es_client, event_group_name, document_index,
                 document_type, topics, id_field_name):
        """
        :param Elasticsearch es_client: The elasticsearch client
        """
        super(ElasticSearchServiceEventCallback, self).__init__()
        self._es_client = es_client
        self._event_group_name = event_group_name
        self._document_index = document_index
        self._document_type = document_type
        self._topics = topics
        self._id_field_name = id_field_name

    def on_event(self, event):
        """
        :param dxlclient.message.Event event: The event
        """
        try:
            event_json = MessageUtils.json_payload_to_dict(event)
        except ValueError:
            logger.error(
                "%s, skipping indexing for topic: %s",
                "Unable to parse event as JSON",
                event.destination_topic)
            return

        document_id = None
        if self._id_field_name:
            document_id = event_json.get(self._id_field_name)
            if not document_id:
                logger.error(
                    "%s from %s field in event, %s: %s",
                    "Unable to obtain id",
                    self._id_field_name,
                    "skipping indexing for topic",
                    event.destination_topic)
                return

        logger.debug("%s. Event: %s, Topic: %s, Index: %s, Type: %s%s.",
                     "Indexing event to elasticsearch",
                     self._event_group_name,
                     event.destination_topic,
                     self._document_index,
                     self._document_type,
                     ", Id: {}".format(document_id) if document_id else "")

        try:
            self._es_client.index(index=self._document_index,
                                  doc_type=self._document_type,
                                  body=event_json,
                                  id=document_id)
        except Exception as e:
            logger.error(
                "%s: %s. Event: %s, Topic: %s, Index: %s, Type: %s%s.",
                "Error indexing event to elasticsearch",
                e.__str__(),
                self._event_group_name,
                event.destination_topic,
                self._document_index,
                self._document_type,
                ", Id: {}".format(document_id) if document_id else "")
            raise
