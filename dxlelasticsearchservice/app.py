from __future__ import absolute_import
import logging
import os

from elasticsearch import Elasticsearch

from dxlbootstrap.app import Application
from dxlclient import ServiceRegistrationInfo
from dxlelasticsearchservice._requesthandlers import \
    ElasticsearchServiceEventCallback, \
    ElasticsearchServiceRequestCallback

# Configure local logger
logger = logging.getLogger(__name__)


class ElasticsearchService(Application):
    """
    The "Elasticsearch DXL Python Service" application class.
    """

    #: The DXL service type for the Elasticsearch API.
    _SERVICE_TYPE = "/opendxl-elasticsearch/service/elasticsearch-api"

    #: The name of the "General" section within the application configuration
    #: file.
    _GENERAL_CONFIG_SECTION = "General"

    #: The property used to specify the list of server name sections in the
    #: application configuration file
    _GENERAL_SERVER_NAMES_CONFIG_PROP = "serverNames"
    #: The property used to specify the list of event group name sections in
    #: the application configuration file
    _GENERAL_EVENT_GROUP_NAMES_CONFIG_PROP = "eventGroupNames"
    #: The property used to specify the list of accessible Elasticsearch APIs
    #: in the application configuration file
    _GENERAL_API_NAMES_CONFIG_PROP = "apiNames"
    #: The property used to specify a unique service discriminator to the
    #: application configuration file. The discriminator, if set, is added to
    #: each of the Elasticsearch API topics registered with the DXL fabric.
    _GENERAL_SERVICE_UNIQUE_ID_PROP = "serviceUniqueId"
    #: The property used to specify in the application configuration file
    #: whether any registered transform scripts should be reloaded if changed
    #: while the service is running.
    _GENERAL_RELOAD_TRANSFORM_SCRIPTS_ON_CHANGE = \
        "reloadTransformScriptsOnChange"

    #: The property used to specify the hostname or IP address of an
    #: Elasticsearch server in the application configuration file.
    _SERVER_HOST_CONFIG_PROP = "host"
    #: The property used to specify the port number of an Elasticsearch
    #: server in the application configuration file.
    _SERVER_PORT_CONFIG_PROP = "port"
    #: The property used to specify in the application configuration file a
    #: prefix to add to the front of the URL path for any requests made to an
    #: Elasticsearch server.
    _SERVER_URL_PREFIX_CONFIG_PROP = "urlPrefix"
    #: The property used to specify in the application configuration file an
    #: username to supply for authentication to the Elasticsearch server.
    _SERVER_USER_CONFIG_PROP = "user"
    #: The property used to specify in the application configuration file a
    #: password to supply for authentication to the Elasticsearch server.
    _SERVER_PASSWORD_CONFIG_PROP = "password"
    #: The property used to specify in the application configuration file
    #: whether or not SSL/TLS should be used when communicating with an
    #: Elasticsearch server.
    _SERVER_USE_SSL_CONFIG_PROP = "useSSL"
    #: The property used to specify in the application configuration file
    #: whether or not the Elasticsearch server certificate was signed by
    #: a valid certificate authority.
    _SERVER_VERIFY_CERTIFICATE_CONFIG_PROP = "verifyCertificate"
    #: The property used to specify in the application configuration file
    #: a path to a bundle of trusted CA certificates to use for validating the
    #: Elasticsearch server's certificate.
    _SERVER_VERIFY_CERT_BUNDLE = "verifyCertBundle"
    #: The property used to specify in the application configuration file
    #: how the name in the Elasticsearch server's certificate should be
    #: validated. If set to "yes" or not specified, the name must match the
    #: value in the "host" setting. If set to "no", the hostname is not
    #: validated. If set to a different value, the hostname must match the
    #: value in the setting. For example, if the value is set to "myserver",
    #: the name in the Elasticsearch server certificate must be "myserver" in
    #: order for the connection to be allowed.
    _SERVER_VERIFY_HOST_NAME = "verifyHostName"
    #: The property used to specify in the application configuration file a
    #: path to a client certificate which is supplied to the Elasticsearch
    #: server for TLS/SSL connections.
    _SERVER_CLIENT_CERTIFICATE = "clientCertificate"
    #: The property used to specify in the application configuration file a
    #: private key to use when making TLS/SSL connnections to an Elasticsearch
    #: server.
    _SERVER_CLIENT_KEY = "clientKey"

    #: The property used to specify in the application configuration file a
    #: list of DXL topic names to associate with the event group.
    _EVENT_GROUP_TOPICS_CONFIG_PROP = "topics"
    #: The property used to specify in the application configuration file the
    #: 'index' in which documents for event group events should be stored
    #: in Elasticsearch.
    _EVENT_GROUP_DOCUMENT_INDEX_PROP = "documentIndex"
    #: The property used to specify in the application configuration file the
    #: 'type' in which documents for event group events should be stored
    #: in Elasticsearch.
    _EVENT_GROUP_DOCUMENT_TYPE_PROP = "documentType"
    #: The property used to specify in the application configuration file the
    #: name of a field in the event payload whose correpsonding value should
    #: be used as the ID of the event group document stored to Elasticsearch.
    _EVENT_GROUP_ID_FIELD_NAME_PROP = "idFieldName"
    #: The property used to specify in the application configuration file a
    #: path to a Python script which will receive the event payload and
    #: optionally transform it into zero, one, or more documents for
    #: storage into Elasticsearch.
    _EVENT_GROUP_TRANSFORM_SCRIPT_PROP = "transformScript"

    def __init__(self, config_dir):
        """
        Constructor parameters:

        :param config_dir: The location of the configuration files for the
            application.
        """
        super(ElasticsearchService,
              self).__init__(config_dir, "dxlelasticsearchservice.config")
        self._api_names = ()
        self._es_client = None
        self._event_groups = {}
        self._service_unique_id = None
        self._reload_transform_scripts_on_change = False

    @property
    def client(self):
        """
        The DXL client used by the application to communicate with the DXL
        fabric.

        :return: The DXL client
        :rtype: dxlclient.client.DxlClient
        """
        return self._dxl_client

    @property
    def config(self):
        """
        The application configuration (as read from the
        "dxlelasticsearchservice.config" file).

        :return: The application configuration
        :rtype: configparser.ConfigParser
        """
        return self._config

    def on_run(self):
        """
        Invoked when the application has started running.
        """
        logger.info("On 'run' callback.")

    def _get_path(self, in_path):
        """
        Returns an absolute path for a file specified in the configuration file
        (supports files relative to the configuration file).

        :param in_path: The specified path
        :return: An absolute path for a file specified in the configuration
            file
        :rtype: str
        """
        if not os.path.isfile(in_path) and not os.path.isabs(in_path):
            config_rel_path = os.path.join(self._config_dir, in_path)
            if os.path.isfile(config_rel_path):
                in_path = config_rel_path
        return in_path

    def _get_setting_from_config(self, section, setting,
                                 default_value=None,
                                 return_type=str,
                                 raise_exception_if_missing=False,
                                 is_file_path=False):
        """
        Get the value for a setting in the application configuration file.

        :param str section: Name of the section in which the setting resides.
        :param str setting: Name of the setting.
        :param default_value: Value to return if the setting is not found in
            the configuration file.
        :param type return_type: Expected 'type' of the value to return.
        :param bool raise_exception_if_missing: Whether or not to raise an
            exception if the setting is missing from the configuration file.
        :param bool is_file_path: Whether or not the value for the setting
            represents a file path. If set to 'True' but a file cannot be
            found for the setting, a ValueError is raised.
        :return: Value for the setting.
        :raises ValueError: If the setting cannot be found in the configuration
            file and 'raise_exception_if_missing' is set to 'True', the
            type of the setting found in the configuration file does not
            match the value specified for 'return_type', or 'is_file_path' is
            set to 'True' but no file can be found which matches the value
            read for the setting.
        """
        config = self.config
        if config.has_option(section, setting):
            getter_methods = {str: config.get,
                              list: config.get,
                              bool: config.getboolean,
                              int: config.getint,
                              float: config.getfloat}
            try:
                return_value = getter_methods[return_type](section, setting)
            except ValueError as ex:
                raise ValueError(
                    "Unexpected value for setting {} in section {}: {}".format(
                        setting, section, ex))
            if return_type == str:
                return_value = return_value.strip()
                if len(return_value) is 0 and raise_exception_if_missing:
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

        if is_file_path and return_value:
            return_value = self._get_path(return_value)
            if not os.path.isfile(return_value):
                raise ValueError(
                    "Cannot find file for setting {} in section {}: {}".format(
                        setting, section, return_value))

        return return_value

    def _get_server_settings(self, server_name):
        """
        Retrieve settings for an Elasticsearch server from the application
        configuration.

        :param str server_name: Name of the server section in the application
            configuration file.
        :return: Dictionary of server settings.
        :rtype: dict
        """
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
                is_file_path=True),
            "client_cert": self._get_setting_from_config(
                server_name, self._SERVER_CLIENT_CERTIFICATE,
                is_file_path=True),
            "client_key": self._get_setting_from_config(
                server_name, self._SERVER_CLIENT_KEY,
                is_file_path=True)}

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
            raise ValueError(
                "{} must be specified in section {} since {} is specified".
                format(self._SERVER_PASSWORD_CONFIG_PROP,
                       server_name,
                       self._SERVER_USER_CONFIG_PROP))
        elif password:
            raise ValueError(
                "{} must be specified in section {} since {} is specified".
                format(self._SERVER_USER_CONFIG_PROP,
                       server_name,
                       self._SERVER_PASSWORD_CONFIG_PROP))

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
        """
        Retrieve settings for an event group from the application
        configuration.

        :param str event_group: Name of the event group section in the
            application configuration file.
        :return: Dictionary of event group settings.
        :rtype: dict
        """
        return {
            "topics": self._get_setting_from_config(
                event_group,
                self._EVENT_GROUP_TOPICS_CONFIG_PROP,
                return_type=list,
                raise_exception_if_missing=True),
            "document_index": self._get_setting_from_config(
                event_group,
                self._EVENT_GROUP_DOCUMENT_INDEX_PROP,
                raise_exception_if_missing=True),
            "document_type": self._get_setting_from_config(
                event_group,
                self._EVENT_GROUP_DOCUMENT_TYPE_PROP,
                raise_exception_if_missing=True),
            "id_field_name": self._get_setting_from_config(
                event_group,
                self._EVENT_GROUP_ID_FIELD_NAME_PROP),
            "transform_script": self._get_setting_from_config(
                event_group,
                self._EVENT_GROUP_TRANSFORM_SCRIPT_PROP,
                is_file_path=True)}

    def on_load_configuration(self, config):
        """
        Invoked after the application-specific configuration has been loaded.

        This callback provides the opportunity for the application to parse
        additional configuration properties.

        :param configparser.ConfigParser config: The application configuration
        """
        logger.info("On 'load configuration' callback.")

        server_names = self._get_setting_from_config(
            self._GENERAL_CONFIG_SECTION,
            self._GENERAL_SERVER_NAMES_CONFIG_PROP,
            return_type=list,
            raise_exception_if_missing=True)
        server_hosts = list(map(self._get_server_settings, server_names))

        event_group_names = self._get_setting_from_config(
            self._GENERAL_CONFIG_SECTION,
            self._GENERAL_EVENT_GROUP_NAMES_CONFIG_PROP,
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
            self._GENERAL_SERVICE_UNIQUE_ID_PROP)

        self._reload_transform_scripts_on_change = \
            self._get_setting_from_config(
                self._GENERAL_CONFIG_SECTION,
                self._GENERAL_RELOAD_TRANSFORM_SCRIPTS_ON_CHANGE,
                return_type=bool,
                default_value=False)

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
            logger.debug("Processing event info for group %s: %s",
                         event_group_name, event_group_info)
            callback = ElasticsearchServiceEventCallback(
                self._es_client,
                event_group_name,
                event_group_info["document_index"],
                event_group_info["document_type"],
                event_group_info["id_field_name"],
                event_group_info["transform_script"],
                self._reload_transform_scripts_on_change)

            for topic in event_group_info["topics"]:
                logger.info("Registering event callback %s for group %s",
                            topic, event_group_name)
                self.add_event_callback(topic,
                                        callback,
                                        separate_thread=True)

    def _get_api_method(self, api_name):
        """
        Retrieve an instance method from the Elasticsearch client object.

        :param str api_name: String name of the instance method object to
            retrieve from the Elasticsearch client object.
        :return: Matching instancemethod if available, else None.
        :rtype: instancemethod
        """
        api_method = None
        if hasattr(self._es_client, api_name):
            api_attr = getattr(self._es_client, api_name)
            if callable(api_attr):
                api_method = api_attr
        return api_method

    def on_register_services(self):
        """
        Invoked when services should be registered with the application
        """
        api_methods = []
        for api_name in self._api_names:
            api_method = self._get_api_method(api_name)
            if api_method:
                api_methods.append(api_method)
            else:
                logger.warning("Elasticsearch API name is invalid: %s",
                               api_name)

        if api_methods:
            logger.info("Registering service: elasticsearch_service")
            service = ServiceRegistrationInfo(
                self._dxl_client,
                self._SERVICE_TYPE)

            for api_method in api_methods:
                api_method_name = api_method.__name__
                topic = "{}{}/{}".format(
                    self._SERVICE_TYPE,
                    "/{}".format(self._service_unique_id)
                    if self._service_unique_id else "",
                    api_method_name)
                logger.info(
                    "Registering request callback: %s%s_%s_%s. Topic: %s.",
                    "elasticsearch",
                    "_{}".format(self._service_unique_id)
                    if self._service_unique_id else "",
                    api_method_name,
                    "requesthandler",
                    topic)
                self.add_request_callback(
                    service,
                    topic,
                    ElasticsearchServiceRequestCallback(self, api_method),
                    False)

            self.register_service(service)
