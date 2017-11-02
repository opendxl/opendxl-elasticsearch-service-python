import logging
import sys
from threading import Lock

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException, TransportError

from dxlbootstrap.util import MessageUtils
from dxlclient.callbacks import EventCallback, RequestCallback
from dxlclient.message import ErrorResponse, Response

# transform scripts are loaded underneath the dxlelasticsearchservice.transform
# module. Including this import to avoid a warning that would otherwise appear
# when the transform scripts are loaded.

import dxlelasticsearchservice.transform

# Python's imp module, used by the dxlelasticsearchservice for loading
# transform scripts, was deprecated in Python 3.4 in favor of importlib
# (see: https://docs.python.org/3/library/imp.html). For later versions of
# Python, the approach documented at
# https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
# is used for loading transform scripts. The `module_from_spec` method used
# by this approach was not supported until Python 3.5. The code below ensures
# that the imp-based loading approach is used for Python versions before 3.5
# whereas the importlib-based loading approach is used for Python 3.5 and
# later.

_PYTHON_VERSION_SUPPORTS_MODULE_FROM_SPEC_LOADING = \
    sys.version_info.major >= 3 and sys.version_info.minor >= 5
if _PYTHON_VERSION_SUPPORTS_MODULE_FROM_SPEC_LOADING:
    import importlib.util
else:
    import imp

# Configure local logger
logger = logging.getLogger(__name__)


class ElasticsearchServiceEventCallback(EventCallback):
    """
    """

    _TRANSFORM_MODULE_BASE_NAME = "dxlelasticsearchservice.transform"

    def __init__(self, es_client, event_group_name, document_index,
                 document_type, topics, id_field_name,
                 transform_script, reload_transform_scripts_on_change):
        """
        :param Elasticsearch es_client: The elasticsearch client
        """
        super(ElasticsearchServiceEventCallback, self).__init__()
        self._es_client = es_client
        self._event_group_name = event_group_name
        self._document_index = document_index
        self._document_type = document_type
        self._topics = topics
        self._id_field_name = id_field_name
        self._transform_script = transform_script

        self._reload_transform_scripts_on_change = \
            reload_transform_scripts_on_change
        if self._transform_script and \
                not self._reload_transform_scripts_on_change:
            self._transform_function = self._get_transform_function()
        else:
            self._transform_function = None
        self._transform_lock = Lock()

    def on_event(self, event):
        """
        :param dxlclient.message.Event event: The event
        """
        if event and event.payload:
            logger.debug("Received event for topic %s. Payload: %s",
                         event.destination_topic, event.payload)

        index_parameters = self._get_index_parameters(event)
        if self._transform_script:
            index_operations = self._get_transformed_operations(
                event, index_parameters)
        else:
            index_operations = [index_parameters]

        for index_operation in index_operations:
            self._log_index_message(logger.debug,
                                    "Indexing event to elasticsearch",
                                    event.destination_topic,
                                    index_operation)
            logger.debug("Indexing with parameters: %s", index_operation)
            try:
                self._es_client.index(**index_operation)
            except Exception:
                self._log_index_message(
                    logger.exception,
                    "Error indexing event to elasticsearch",
                    event.destination_topic,
                    index_operation)
                raise

    def _get_transformed_operations(self, event, index_parameters):
        if self._reload_transform_scripts_on_change:
            with self._transform_lock:
                index_operations = self._get_transform_function()(
                    event, index_parameters)
        else:
            transform_function = self._transform_function
            index_operations = transform_function(event, index_parameters)

        if isinstance(index_operations, dict):
            index_operations = [index_operations]

        return index_operations

    def _get_transform_function(self):
        full_module_name = "{}.{}".format(self._TRANSFORM_MODULE_BASE_NAME,
                                          self._event_group_name)

        logger.debug("Loading %s from %s", full_module_name,
                     self._transform_script)
        try:
            # See the definition of the
            # _PYTHON_VERSION_SUPPORTS_MODULE_FROM_SPEC_LOADING constant
            # for more details on why the different loading approaches are
            # used.
            if _PYTHON_VERSION_SUPPORTS_MODULE_FROM_SPEC_LOADING:
                spec = importlib.util.spec_from_file_location(
                    full_module_name, self._transform_script)
                transform_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(transform_module)
            else:
                transform_module = imp.load_source(full_module_name,
                                                   self._transform_script)
        except Exception as e:
            logger.error(
                "Failed to load transform script (%s) from section %s: %s",
                self._transform_script, self._event_group_name, str(e))
            raise

        transform_function = transform_module.__dict__.get("on_event")
        if not transform_function:
            raise ValueError(
                "%s in transform script (%s) from section %s",
                "on_event function not found",
                self._transform_script,
                self._event_group_name)

        return transform_function

    def _get_index_parameters(self, event):
        body = None
        document_id = None

        try:
            body = MessageUtils.json_payload_to_dict(event)
            if self._id_field_name:
                document_id = body.get(self._id_field_name)
                if not document_id:
                    logger.error(
                        "%s from %s field in event, %s: %s",
                        "Unable to obtain id",
                        self._id_field_name,
                        "skipping indexing for topic",
                        event.destination_topic)
        except ValueError:
            if self._transform_script:
                body = event.payload
            else:
                logger.error(
                    "%s, skipping indexing for topic: %s",
                    "Unable to parse event payload as JSON",
                    event.destination_topic)

        if body:
            index_parameters = {"index": self._document_index,
                                "doc_type": self._document_type,
                                "body": body,
                                "id": document_id}
        else:
            index_parameters = None

        return index_parameters

    @staticmethod
    def _get_index_parameter_text(operation, name, description):
        value = operation.get(name)
        return ", {}: {}".format(description,
                                 value if value else "<None>")

    def _log_index_message(self, log_function, message, topic,
                           index_operation):
        log_function("%s. Event: %s, Topic: %s%s%s%s.",
                     message,
                     self._event_group_name,
                     topic,
                     self._get_index_parameter_text(index_operation,
                                                    "index",
                                                    "Index"),
                     self._get_index_parameter_text(index_operation,
                                                    "doc_type",
                                                    "Type"),
                     self._get_index_parameter_text(index_operation,
                                                    "id",
                                                    "ID"))


class ElasticsearchServiceRequestCallback(RequestCallback):
    """
    """
    def __init__(self, app, api_method):
        super(ElasticsearchServiceRequestCallback, self).__init__()
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
