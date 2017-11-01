import logging
import os

from elasticsearch import Elasticsearch

from dxlbootstrap.app import Application
from dxlclient import ServiceRegistrationInfo
from dxlelasticsearchservice._requesthandlers import \
    ElasticSearchServiceEventCallback, \
    ElasticSearchServiceRequestCallback

# Configure local logger
logger = logging.getLogger(__name__)


class ElasticSearchService(Application):
    """
    The "OpenDXL Elasticsearch Service" application class.
    """

    _SERVICE_TYPE = "/opendxl-elasticsearch/service/elasticsearch-api"

    _GENERAL_CONFIG_SECTION = "General"

    _GENERAL_SERVER_NAMES_CONFIG_PROP = "serverNames"
    _GENERAL_EVENT_NAMES_CONFIG_PROP = "eventNames"
    _GENERAL_API_NAMES_CONFIG_PROP = "apiNames"
    _GENERAL_SERVICE_UNIQUE_ID_PROP = "serviceUniqueId"

    _SERVER_HOST_CONFIG_PROP = "host"
    _SERVER_PORT_CONFIG_PROP = "port"
    _SERVER_URL_PREFIX_CONFIG_PROP = "urlPrefix"
    _SERVER_USER_CONFIG_PROP = "user"
    _SERVER_PASSWORD_CONFIG_PROP = "password"
    _SERVER_USE_SSL_CONFIG_PROP = "useSSL"
    _SERVER_VERIFY_CERTIFICATE_CONFIG_PROP = "verifyCertificate"
    _SERVER_VERIFY_CERT_BUNDLE = "verifyCertBundle"
    _SERVER_VERIFY_HOST_NAME = "verifyHostName"
    _SERVER_CLIENT_CERTIFICATE = "clientCertificate"
    _SERVER_CLIENT_KEY = "clientKey"

    _EVENT_TOPICS_CONFIG_PROP = "topics"
    _EVENT_DOCUMENT_INDEX_PROP = "documentIndex"
    _EVENT_DOCUMENT_TYPE_PROP = "documentType"
    _EVENT_ID_FIELD_NAME_PROP = "idFieldName"

    def __init__(self, config_dir):
        """
        Constructor parameters:

        :param config_dir: The location of the configuration files for the
            application
        """
        super(ElasticSearchService,
              self).__init__(config_dir, "dxlelasticsearchservice.config")
        self._es_client = None

    @property
    def client(self):
        """
        The DXL client used by the application to communicate with the DXL
        fabric
        """
        return self._dxl_client

    @property
    def config(self):
        """
        The application configuration (as read from the "dxlelasticsearchservice.config" file)
        """
        return self._config

    def on_run(self):
        """
        Invoked when the application has started running.
        """
        logger.info("On 'run' callback.")

    def _get_setting_from_config(self, section, setting,
                                 default_value=None,
                                 return_type=str,
                                 raise_exception_if_missing=False,
                                 verify_file_path=False):
        """

        :param section:
        :param setting:
        :param default_value:
        :param type return_type:
        :param raise_exception_if_missing:
        :return:
        """
        config = self._config
        if self.config.has_option(section, setting):
            getter_methods = {str: config.get,
                              list: config.get,
                              bool: config.getboolean,
                              int: config.getint,
                              float: config.getfloat}
            try:
                return_value = getter_methods[return_type](section, setting)
            except ValueError as e:
                raise ValueError(
                    "Unexpected value for setting {} in section {}: {}".format(
                        setting, section, e.message))
            if return_type == str:
                return_value = return_value.strip()
                if len(return_value) is 0:
                    raise ValueError(
                        "Required setting {} in section {} is empty".format(
                            setting, section))
            elif return_type == list:
                return_value = [item.strip()
                                for item in return_value.split(",")]
                if len(return_value) is 1 and len(return_value[0]) is 0 \
                        and raise_exception_if_missing:
                    raise ValueError(
                        "Required setting {} in section {} is empty".format(
                            setting, section))
        elif raise_exception_if_missing:
            raise ValueError(
                "Required setting {} not found in {} section".format(setting,
                                                                     section))
        else:
            return_value = default_value

        if verify_file_path \
                and return_value is not None and \
                not os.access(return_value, os.R_OK):
            raise ValueError(
                "Cannot read file for setting {} in section {}: {}".format(
                    setting, section, return_value))

        return return_value

    def _get_server_settings(self, server_name):
        server = {
            "host": self._get_setting_from_config(
                server_name, self._SERVER_HOST_CONFIG_PROP,
                raise_exception_if_missing=True)}

        optional_settings = {
            "port": self._get_setting_from_config(
                server_name, self._SERVER_PORT_CONFIG_PROP, return_type=int),
            "url_prefix": self._get_setting_from_config(
                server_name, self._SERVER_URL_PREFIX_CONFIG_PROP),
            "use_ssl": self._get_setting_from_config(
                server_name, self._SERVER_USE_SSL_CONFIG_PROP,
                return_type=bool),
            "verify_certs": self._get_setting_from_config(
                server_name, self._SERVER_VERIFY_CERTIFICATE_CONFIG_PROP,
                return_type=bool),
            "ca_certs": self._get_setting_from_config(
                server_name, self._SERVER_VERIFY_CERT_BUNDLE,
                verify_file_path=True),
            "client_cert": self._get_setting_from_config(
                server_name, self._SERVER_CLIENT_CERTIFICATE,
                verify_file_path=True),
            "client_key": self._get_setting_from_config(
                server_name, self._SERVER_CLIENT_KEY,
                verify_file_path=True)}

        for key, value in optional_settings.items():
            if value is not None:
                server[key] = value

        user = self._get_setting_from_config(server_name,
                                             self._SERVER_USER_CONFIG_PROP)
        password = self._get_setting_from_config(
            server_name, self._SERVER_PASSWORD_CONFIG_PROP)

        if user and password:
            server["http_auth"] = (user, password)
        elif user:
            raise Exception(
                "Password must be specified if user is specified")
        elif password:
            raise Exception(
                "Password must be specified if user is specified")

        try:
            verify_host_name = self._get_setting_from_config(
                server_name, self._SERVER_VERIFY_HOST_NAME,
                return_type=bool)
            # elasticsearch treats `True` as a bool variable to match
            # against the server hostname. Converting this to `None` instead
            # to enable verification of the host name without matching it
            # to a specific value.
            if verify_host_name:
                verify_host_name = None
        except ValueError:
            # If the hostname cannot be coerced into a bool, assume it
            # might be a string representing the exact hostname to be
            # matched.
            verify_host_name = self._get_setting_from_config(
                server_name, self._SERVER_VERIFY_HOST_NAME,
                return_type=str)
        server["ssl_assert_hostname"] = verify_host_name

        return server

    def _get_event_group_settings(self, event_group):
        return {
            "topics": self._get_setting_from_config(
                event_group,
                self._EVENT_TOPICS_CONFIG_PROP,
                return_type=list,
                raise_exception_if_missing=True),
            "documentIndex": self._get_setting_from_config(
                event_group,
                self._EVENT_DOCUMENT_INDEX_PROP,
                raise_exception_if_missing=True),
            "documentType": self._get_setting_from_config(
                event_group,
                self._EVENT_DOCUMENT_TYPE_PROP,
                raise_exception_if_missing=True),
            "idFieldName": self._get_setting_from_config(
                event_group,
                self._EVENT_ID_FIELD_NAME_PROP)}

    def on_load_configuration(self, config):
        """
        Invoked after the application-specific configuration has been loaded

        This callback provides the opportunity for the application to parse
        additional configuration properties.

        :param config: The application configuration
        """
        logger.info("On 'load configuration' callback.")

        server_names = self._get_setting_from_config(
            self._GENERAL_CONFIG_SECTION,
            self._GENERAL_SERVER_NAMES_CONFIG_PROP,
            return_type=list,
            raise_exception_if_missing=True)
        server_hosts = map(self._get_server_settings, server_names)

        event_group_names = self._get_setting_from_config(
            self._GENERAL_CONFIG_SECTION,
            self._GENERAL_EVENT_NAMES_CONFIG_PROP,
            return_type=list,
            default_value=[])
        self._event_groups = \
            {event_group_name: self._get_event_group_settings(event_group_name)
             for event_group_name in event_group_names}

        self._api_names = self._get_setting_from_config(
            self._GENERAL_CONFIG_SECTION,
            self._GENERAL_API_NAMES_CONFIG_PROP,
            return_type=list,
            default_value=[])

        self._service_unique_id = self._get_setting_from_config(
            self._GENERAL_CONFIG_SECTION,
            self._GENERAL_SERVICE_UNIQUE_ID_PROP,
            default_value=server_names[0] \
                if len(server_names) == 1 else None)

        logger.debug("Server host settings: %s", server_hosts)
        self._es_client = Elasticsearch(server_hosts)

    def on_dxl_connect(self):
        """
        Invoked after the client associated with the application has connected
        to the DXL fabric.
        """
        logger.info("On 'DXL connect' callback.")

    def on_register_event_handlers(self):
        """
        Invoked when event handlers should be registered with the application
        """
        for event_group_name, event_group_info in self._event_groups.items():
            callback = ElasticSearchServiceEventCallback(
                self._es_client,
                event_group_name,
                event_group_info["documentIndex"],
                event_group_info["documentType"],
                event_group_info["topics"],
                event_group_info["idFieldName"])
            for topic in event_group_info["topics"]:
                logger.info("Registering event callback %s for group %s",
                            topic, event_group_name)
                self.add_event_callback(topic,
                                        callback,
                                        separate_thread=False)

    def _get_api_method(self, apis_so_far, api_name):
        valid_api_name = False
        if hasattr(self._es_client, api_name):
            api_attr = getattr(self._es_client, api_name)
            if callable(api_attr):
                valid_api_name = True
                apis_so_far.append(api_attr)
        if not valid_api_name:
            logger.warning("Elasticsearch API name is invalid: %s", api_name)
        return apis_so_far

    def on_register_services(self):
        """
        Invoked when services should be registered with the application
        """
        api_methods = reduce(self._get_api_method, self._api_names, [])

        if api_methods:
            if not self._service_unique_id:
                raise ValueError(
                    "Required setting {} in section {} is empty".format(
                        "serviceUniqueId", self._GENERAL_CONFIG_SECTION))

            logger.info("Registering service: elasticsearch_service")
            service = ServiceRegistrationInfo(
                self._dxl_client,
                self._SERVICE_TYPE)

            for api_method in api_methods:
                api_method_name = api_method.__name__
                logger.info("Registering request callback: %s_%s_%s_%s",
                            "elasticsearch",
                            self._service_unique_id,
                            api_method_name,
                            "requesthandler")
                self.add_request_callback(
                    service,
                    "{}/{}/{}".format(self._SERVICE_TYPE,
                                      self._service_unique_id,
                                      api_method_name),
                    ElasticSearchServiceRequestCallback(self, api_method),
                    False)

            self.register_service(service)
