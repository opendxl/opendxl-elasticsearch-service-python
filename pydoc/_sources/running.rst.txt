Running
=======

Once the application library has been installed and the configuration files are populated it can be started by
executing the following command line:

    .. code-block:: shell

        python -m dxlelasticsearchservice <configuration-directory>

    The ``<configuration-directory>`` argument must point to a directory containing the configuration files
    required for the application (see :doc:`configuration`).

For example:

    .. code-block:: shell

        python -m dxlelasticsearchservice config

For running the server in conjunction with the samples, use the configuration
in the ``sample`` sub-directory:

    .. code-block:: shell

        python -m dxlelasticsearchservice sample

Output
------

The output from starting the service with the ``sample`` sub-directory
configuration should appear similar to the following:

    .. code-block:: shell

        Running application ...
        On 'run' callback.
        On 'load configuration' callback.
        Incoming message configuration: queueSize=1000, threadCount=10
        Message callback configuration: queueSize=1000, threadCount=10
        Attempting to connect to DXL fabric ...
        Connected to DXL fabric.
        Registering event callback /sample/elasticsearch/advancedtransform for group advanced_transform_example
        Registering event callback /sample/elasticsearch/basicevent for group basic_event_example
        Registering service: elasticsearch_service
        Registering request callback: elasticsearch_index_requesthandler. Topic: /opendxl-elasticsearch/service/elasticsearch-api/index.
        Registering request callback: elasticsearch_get_requesthandler. Topic: /opendxl-elasticsearch/service/elasticsearch-api/get.
        Registering request callback: elasticsearch_update_requesthandler. Topic: /opendxl-elasticsearch/service/elasticsearch-api/update.
        Registering request callback: elasticsearch_delete_requesthandler. Topic: /opendxl-elasticsearch/service/elasticsearch-api/delete.
        On 'DXL connect' callback.
