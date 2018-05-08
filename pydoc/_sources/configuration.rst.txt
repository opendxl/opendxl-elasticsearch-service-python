Configuration
=============

The Elasticsearch DXL Python Service application requires a set of configuration files to operate.

This distribution contains a ``config`` sub-directory that includes the configuration files that must
be populated prior to running the application.

Each of these files are documented throughout the remainder of this page.

Application configuration directory:

    .. code-block:: python

        config/
            dxlclient.config
            dxlelasticsearchservice.config
            logging.config (optional)

.. _dxl_client_config_file_label:

DXL Client Configuration File (dxlclient.config)
------------------------------------------------

    The required ``dxlclient.config`` file is used to configure the DXL client that will connect to the DXL fabric.

    The steps to populate this configuration file are the same as those documented in the `OpenDXL Python
    SDK`, see the
    `OpenDXL Python SDK Samples Configuration <https://opendxl.github.io/opendxl-client-python/pydoc/sampleconfig.html>`_
    page for more information.

    The following is an example of a populated DXL client configuration file:

        .. code-block:: python

            [Certs]
            BrokerCertChain=c:\\certificates\\brokercerts.crt
            CertFile=c:\\certificates\\client.crt
            PrivateKey=c:\\certificates\\client.key

            [Brokers]
            {5d73b77f-8c4b-4ae0-b437-febd12facfd4}={5d73b77f-8c4b-4ae0-b437-febd12facfd4};8883;mybroker.mcafee.com;192.168.1.12
            {24397e4d-645f-4f2f-974f-f98c55bdddf7}={24397e4d-645f-4f2f-974f-f98c55bdddf7};8883;mybroker2.mcafee.com;192.168.1.13

.. _dxl_service_config_file_label:

Elasticsearch DXL Python Service (dxlelasticsearchservice.config)
-----------------------------------------------------------------

    The required ``dxlelasticsearchservice.config`` file is used to configure
    the application.

    The following is an example of a populated application configuration file:

        .. code-block:: ini

            [General]
            serverNames=es1
            eventGroupNames=eventgroup1
            apiNames=index,get,update,delete

            [es1]
            host=elasticserver1
            user=elastic
            password=elasticpassword
            useSSL=yes
            verifyCertificate=yes
            verifyCertBundle=esCA.crt
            verifyHostName=yes
            clientCertificate=client1.crt
            clientKey=client1.key

            [eventgroup1]
            topics=/myservice/mytopic1,/myservice/mytopic2
            documentIndex=opendxl-services
            documentType=myservice
            idFieldName=event_id
            transformScript=transform.py


    **General**

        The ``[General]`` section is used to specify the list of Elasticsearch
        servers, Elasticsearch methods which should be available to invoke via
        DXL, and information for DXL event notifications which should be stored
        to Elasticsearch.

        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | Name                             | Required | Description                                                                                            |
        +==================================+==========+========================================================================================================+
        | serviceUniqueId                  | no       | An optional unique identifier used to identify the                                                     |
        |                                  |          | opendxl-elasticsearch service on the DXL fabric. If set, this                                          |
        |                                  |          | unique identifier will be appended to the name of each request                                         |
        |                                  |          | topic added to the fabric. For example, if the serviceUniqueId is                                      |
        |                                  |          | set to ``sample``, the request topic names would start with the                                        |
        |                                  |          | following:                                                                                             |
        |                                  |          |                                                                                                        |
        |                                  |          | ``/opendxl-elasticsearch/service/elasticsearch-api/sample/<method>``                                   |
        |                                  |          |                                                                                                        |
        |                                  |          | If serviceUniqueId is not set, request topic names would not                                           |
        |                                  |          | include an id segment, for example:                                                                    |
        |                                  |          |                                                                                                        |
        |                                  |          | ``/opendxl-elasticsearch/service/elasticsearch-api/<method>``                                          |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | serverNames                      | yes      | The list of Elasticsearch servers to expose to the DXL fabric,                                         |
        |                                  |          | delimited by commas.                                                                                   |
        |                                  |          |                                                                                                        |
        |                                  |          | For example: ``es1,es2,es3``                                                                           |
        |                                  |          |                                                                                                        |
        |                                  |          | For each name specified, a corresponding section must be defined within                                |
        |                                  |          | this configuration file that provides detailed information about the                                   |
        |                                  |          | server (see "Server Section" below).                                                                   |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | eventGroupNames                  | no       | The list of event groups for which any DXL events received are indexed                                 |
        |                                  |          | to Elasticsearch, delimited by commas.                                                                 |
        |                                  |          |                                                                                                        |
        |                                  |          | For example: ``eventgroup1,eventgroup2,eventgroup3``                                                   |
        |                                  |          |                                                                                                        |
        |                                  |          | For each name specified, a corresponding section must be defined within                                |
        |                                  |          | this configuration file that provides detailed information about the                                   |
        |                                  |          | event group (see "Event Group Section" below).                                                         |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | apiNames                         | no       | The list of Elasticsearch APIs for which corresponding request topics                                  |
        |                                  |          | should be exposed to the DXL fabric.                                                                   |
        |                                  |          |                                                                                                        |
        |                                  |          | For example: ``index,get,update,delete``                                                               |
        |                                  |          |                                                                                                        |
        |                                  |          | With this example and the ``serviceUniqueId`` setting set to                                           |
        |                                  |          | ``sample``, the request topics exposed to the DXL fabric would be:                                     |
        |                                  |          |                                                                                                        |
        |                                  |          | ``/opendxl-elasticsearch/service/elasticsearch-api/sample/index``                                      |
        |                                  |          |                                                                                                        |
        |                                  |          | ``/opendxl-elasticsearch/service/elasticsearch-api/sample/get``                                        |
        |                                  |          |                                                                                                        |
        |                                  |          | ``/opendxl-elasticsearch/service/elasticsearch-api/sample/update``                                     |
        |                                  |          |                                                                                                        |
        |                                  |          | ``/opendxl-elasticsearch/service/elasticsearch-api/sample/delete``                                     |
        |                                  |          |                                                                                                        |
        |                                  |          | The total list of available API method names and parameters is at:                                     |
        |                                  |          |                                                                                                        |
        |                                  |          | https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch                               |
        |                                  |          |                                                                                                        |
        |                                  |          | For each name specified, a corresponding section must be defined within                                |
        |                                  |          | this configuration file that provides detailed information about the                                   |
        |                                  |          | event group.                                                                                           |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | reloadTransformScriptsOnChange   | no       | Controls whether or not changes made to event group transform scripts while the service is running can |
        |                                  |          | be reloaded dynamically. Setting this to ``yes`` can be helpful to reduce service restarts while       |
        |                                  |          | developing a transform script.                                                                         |
        |                                  |          |                                                                                                        |
        |                                  |          | Defaults to ``no``, load transform scripts only at service startup time.                               |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+

    **Server Section (1 per Elasticsearch server)**

        Each server specified in the ``serverNames`` property of the ``[General]`` section must have a
        section defined which contains details about the particular Elasticsearch server.

        The section name must match the name of the server in the ``serverNames`` property (for example: ``[es1]``).

        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | Name                             | Required | Description                                                                                            |
        +==================================+==========+========================================================================================================+
        | host                             | yes      | The Elasticsearch server hostname or IP address.                                                       |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | port                             | no       | The Elasticsearch server HTTP API port. Defaults to ``9200``.                                          |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | urlPrefix                        | no       | The URL prefix under which the Elasticsearch server's HTTP API                                         |
        |                                  |          | is hosted. For example, if this were set to ``api``, requests that                                     |
        |                                  |          | the OpenDXL Elasticsearch service makes to the Elasticsearch                                           |
        |                                  |          | server would start with the following:                                                                 |
        |                                  |          |                                                                                                        |
        |                                  |          | ``http(s)://<host>:<port>/api``                                                                        |
        |                                  |          |                                                                                                        |
        |                                  |          | Defaults to no prefix, making requests to the root path.                                               |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | user                             | no       | The name of the user used when making requests to the                                                  |
        |                                  |          | Elasticsearch server. Defaults to no user name. Required if                                            |
        |                                  |          | ``password`` is specified.                                                                             |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | password                         | no       | The password associated with the user used when making requests                                        |
        |                                  |          | to the Elasticsearch server. Defaults to no password. Required                                         |
        |                                  |          | if ``user`` is specified.                                                                              |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | useSSL                           | no       | Whether or not to use SSL/TLS for requests made to the                                                 |
        |                                  |          | Elasticsearch server. If set to ``yes``, SSL/TLS is used.                                              |
        |                                  |          | Defaults to ``no``.                                                                                    |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | verifyCertificate                | no       | Whether to verify that Elasticsearch server's certificate was                                          |
        |                                  |          | signed by a valid certificate authority when SSL/TLS is being                                          |
        |                                  |          | used. Defaults to ``yes``.                                                                             |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | verifyCertBundle                 | no       | A path to a CA Bundle file containing certificates of trusted                                          |
        |                                  |          | CAs. The CA Bundle is used to ensure that the Elasticsearch                                            |
        |                                  |          | server being connected to was signed by a valid authority. Only                                        |
        |                                  |          | applicable if ``verifyCertificate`` is ``yes``.                                                        |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | verifyHostName                   | no       | Controls how the name in the Elasticsearch server's certificate                                        |
        |                                  |          | is validated if SSL/TLS is being used. If set to ``yes`` or not                                        |
        |                                  |          | specified, the name must match the value in the ``host``                                               |
        |                                  |          | setting. If set to ``no``, the hostname is not validated. If set                                       |
        |                                  |          | to a different value, the hostname must match the value in the                                         |
        |                                  |          | setting. For example, if the value is set to ``myserver``, the                                         |
        |                                  |          | name in the Elasticsearch server certificate must be                                                   |
        |                                  |          | ``myserver`` in order for the connection to be allowed.                                                |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | clientCertificate                | no       | A path to a client certificate supplied to the Elasticsearch                                           |
        |                                  |          | server for TLS/SSL connections. Defaults to not using a client                                         |
        |                                  |          | certificate.                                                                                           |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+
        | clientKey                        | no       | A path to a client private key used for TLS/SSL connections made                                       |
        |                                  |          | to the Elasticsearch server. Defaults to not using a client                                            |
        |                                  |          | private key.                                                                                           |
        +----------------------------------+----------+--------------------------------------------------------------------------------------------------------+

    **Event Group Section (1 per event group)**

        Each event group specified in the ``eventGroupNames`` property of the ``[General]`` section must have a
        section defined which contains details about the particular event group.

        The section name must match the name of the event group in the ``eventGroupNames`` property (for example:
        ``[eventgroup1]``).

        +----------------------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
        | Name                             | Required | Description                                                                                                                                           |
        +==================================+==========+=======================================================================================================================================================+
        | topics                           | yes      | The list of topics to subscribe to the DXL fabric for event                                                                                           |
        |                                  |          | notifications, delimited by commas.                                                                                                                   |
        |                                  |          |                                                                                                                                                       |
        |                                  |          | For example: ``es1,es2,es3``                                                                                                                          |
        |                                  |          |                                                                                                                                                       |
        |                                  |          | For each event notification received, corresponding documents                                                                                         |
        |                                  |          | with the event payload are indexed to Elasticsearch.                                                                                                  |
        +----------------------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
        | documentIndex                    | yes      | Index to use in storing the event document to Elasticsearch.                                                                                          |
        |                                  |          | See the                                                                                                                                               |
        |                                  |          | `ElasticSearch Index API Documentation <https://www.elastic.co/guide/en/elasticsearch/guide/current/_document_metadata.html#_index>`__                |
        |                                  |          | for additional details.                                                                                                                               |
        +----------------------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
        | documentType                     | yes      | Type of the document to store to Elasticsearch.                                                                                                       |
        |                                  |          | See the                                                                                                                                               |
        |                                  |          | `ElasticSearch Type API Documentation <https://www.elastic.co/guide/en/elasticsearch/guide/current/_document_metadata.html#_type>`__                  |
        |                                  |          | for additional details.                                                                                                                               |
        +----------------------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
        | idFieldName                      | no       | Name of the field in the event payload whose corresponding value                                                                                      |
        |                                  |          | should be used as the ID of the document stored to                                                                                                    |
        |                                  |          | Elasticsearch. See the                                                                                                                                |
        |                                  |          | `Elasticsearch Id API Documentation <https://www.elastic.co/guide/en/elasticsearch/guide/current/_document_metadata.html#_id>`__                      |
        |                                  |          | for additional details.                                                                                                                               |
        |                                  |          | Defaults to using an unique ID that Elasticsearch automatically                                                                                       |
        |                                  |          | generates.                                                                                                                                            |
        |                                  |          |                                                                                                                                                       |
        |                                  |          | For example, an event payload may have the following content:                                                                                         |
        |                                  |          |                                                                                                                                                       |
        |                                  |          | .. code-block:: json                                                                                                                                  |
        |                                  |          |                                                                                                                                                       |
        |                                  |          |     { "myid": "12345",                                                                                                                                |
        |                                  |          |       "mytext": "hello world" }                                                                                                                       |
        |                                  |          |                                                                                                                                                       |
        |                                  |          | If idFieldName is set to ``myid``, the value ``12345`` would                                                                                          |
        |                                  |          | be extracted from the payload and used as the document ID. If                                                                                         |
        |                                  |          | idFieldName is set but the value cannot be found in the event                                                                                         |
        |                                  |          | payload, the document will not be stored.                                                                                                             |
        |                                  |          |                                                                                                                                                       |
        |                                  |          | **NOTE: The idFieldName can currently only refer to a key                                                                                             |
        |                                  |          | which exists at the top-level of the event payload. In order                                                                                          |
        |                                  |          | to map the ID from a field which appears in a nested                                                                                                  |
        |                                  |          | structure in the event payload, a "transformScript" would                                                                                             |
        |                                  |          | need to be used.**                                                                                                                                    |
        +----------------------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
        | transformScript                  | no       | Path to a Python script which will receive the event payload and                                                                                      |
        |                                  |          | optionally transform it into documents to be stored into                                                                                              |
        |                                  |          | Elasticsearch. The transform script must define an ``on_event``                                                                                       |
        |                                  |          | function which accepts two parameters: the                                                                                                            |
        |                                  |          | ``dxlclient.message.Event`` object received for the event                                                                                             |
        |                                  |          | callback and a dictionary containing a default set of parameters                                                                                      |
        |                                  |          | for a corresponding document to be stored to Elasticsearch.                                                                                           |
        +----------------------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------+

Logging File (logging.config)
-----------------------------

    The optional ``logging.config`` file is used to configure how the application writes log messages.
