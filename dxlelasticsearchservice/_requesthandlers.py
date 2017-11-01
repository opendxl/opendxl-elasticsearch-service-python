import logging

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException, TransportError

from dxlbootstrap.util import MessageUtils
from dxlclient.callbacks import EventCallback, RequestCallback
from dxlclient.message import ErrorResponse, Response

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
        if event and event.payload:
            logger.debug("Received event for topic %s. Payload: %s",
                         event.destination_topic, event.payload)

        try:
            event_json = MessageUtils.json_payload_to_dict(event)
        except ValueError:
            logger.error(
                "%s, skipping indexing for topic: %s",
                "Unable to parse event payload as JSON",
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
            logger.exception(
                "%s: %s. Event: %s, Topic: %s, Index: %s, Type: %s%s.",
                "Error indexing event to elasticsearch",
                str(e),
                self._event_group_name,
                event.destination_topic,
                self._document_index,
                self._document_type,
                ", Id: {}".format(document_id) if document_id else "")


class ElasticSearchServiceRequestCallback(RequestCallback):
    """
    """
    def __init__(self, app, api_method):
        super(ElasticSearchServiceRequestCallback, self).__init__()
        self._app = app
        self._api_method = api_method

    def on_request(self, request):
        """
        :param dxlclient.message.Request request: The request
        """
        MessageUtils.decode_payload(request)
        logger.info("Request received on topic '%s'",
                    request.destination_topic)
        logger.debug("Payload for topic %s: %s", request.destination_topic,
                     request.payload)
        try:
            res = Response(request)

            request_dict = MessageUtils.json_payload_to_dict(request) \
                if request.payload else {}

            response_data = self._api_method(**request_dict)
            MessageUtils.dict_to_json_payload(res, response_data)

        except ElasticsearchException as ex:
            error_str = str(ex)
            logger.exception("Elasticsearch exception handling request: %s",
                             error_str)
            res = ErrorResponse(
                request,
                error_message=MessageUtils.encode(error_str))
            error_dict = {
                "module": ex.__module__,
                "class": ex.__class__.__name__}
            if isinstance(ex, TransportError):
                error_dict["data"] = {"status_code": ex.status_code,
                                      "error": ex.error,
                                      "info": ex.info}
            MessageUtils.dict_to_json_payload(res, error_dict)

        except Exception as ex:
            error_str = str(ex)
            logger.exception("Error handling request: %s", error_str)
            if not error_str:
                error_str = ex.__class__.__name__
            res = ErrorResponse(request,
                                error_message=MessageUtils.encode(error_str))

        self._app.client.send_response(res)
