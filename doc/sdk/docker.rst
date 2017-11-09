Docker Support
==============

A pre-built Docker image can be used as an alternative to installing a Python environment with the libraries required
for the Elasticsearch DXL Python service. Docker images for the Elasticsearch DXL Python service are posted to the
following Docker repository:

`<https://hub.docker.com/r/opendxl/opendxl-elasticsearch-service-python/>`_

The remainder of this page walks through the steps required to configure the service,
pull the image from the repository, and run the Elasticsearch DXL service via a Docker container.

Service Configuration
---------------------

The first step is to connect to the host that is running Docker and configure the Elasticsearch DXL Python service. The
configuration files that are required for the Elasticsearch DXL Python service will reside on the host system and be
made available to the Docker container via a data volume.

Once you have logged into the host system, perform the following steps:

    1.) Create a directory to contain the configuration files

        .. container:: note, admonition

            mkdir dxlelasticsearchservice-config

    2.) Change to the newly created directory

        .. container:: note, admonition

            cd dxlelasticsearchservice-config

    3.) Download the latest configuration files for the Elasticsearch DXL Python service

        The latest release of the service can be found at the following page:

        `<https://github.com/opendxl/opendxl-elasticsearch-service-python/releases/latest>`_

        Download the latest configuration package (dxlelasticsearchservice-python-dist-config). For example:

        .. container:: note, admonition

           wget ht\ tps://github.com/opendxl/opendxl-elasticsearch-service-python/releases/download/\ |version|\/dxlelasticsearchservice-python-dist-config-\ |version|\.zip

    4.) Extract the configuration package

        .. container:: note, admonition

           unzip dxlelasticsearchservice-python-dist-config-\ |version|\.zip

    5.) Populate the configuration files:

        * :ref:`Client Configuration File <dxl_client_config_file_label>`
        * :ref:`Service Configuration File <dxl_service_config_file_label>`

Pull Docker Image
-----------------

The next step is to `pull` the Elasticsearch DXL Python service image from the Docker repository.

The image can be pulled using the following Docker command:

    :literal:`docker pull opendxl/opendxl-elasticsearch-service-python:<release-version>`

    The following parameters must be specified:

        * ``release-version``
          The release version of the Elasticsearch DXL Python service

For example:

    .. container:: note, admonition

        docker pull opendxl/opendxl-elasticsearch-service-python:\ |version|\

Create Docker Container
-----------------------

The final step is to create a Docker container based on the pulled image.

The container can be created using the following Docker command:

    :literal:`docker run -d --name dxlelasticsearchservice -v <host-config-dir>:/opt/dxlelasticsearchservice-config opendxl/opendxl-elasticsearch-service-python:<release-version>`

    The following parameters must be specified:

        * ``host-config-dir``
          The directory on the host that contains the service configuration files
        * ``release-version``
          The version of the image (See "Pull Docker Image" section above)

For example:

    .. container:: note, admonition

        docker run -d --name dxlelasticsearchservice -v /home/myuser/dxlelasticsearchservice-config:/opt/dxlelasticsearchservice-config opendxl/opendxl-elasticsearch-service-python:\ |version|\

**Note:** A restart policy can be specified via the restart flag (``--restart <policy>``). This flag can be used to restart
the container when the system reboots or if the service terminates abnormally. The ``unless-stopped`` policy will
restart the container unless it has been explicitly stopped.

Additional Docker Commands
--------------------------

The following Docker commands are useful once the container has been created.

    * **Container Status**

        The ``ps`` command can be used to show the status of the container.

            :literal:`docker ps --filter name=dxlelasticsearchservice`

        Example output:

            .. parsed-literal::

                CONTAINER ID  COMMAND                 CREATED        STATUS
                c60eaf0788fe  "python -m dxlelas..."  7 minutes ago  Up 7 minutes

    * **Container Logs**

        The ``logs`` command can be used to display the log messages for the container.

            :literal:`docker logs dxlelasticsearchservice`

        Example output:

            .. parsed-literal::

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

        The log output can be `followed` by adding a ``-f`` flag (similar to tail) to the logs command.

    * **Stop/Restart/Start**

        The container can be stopped, restarted, and started using the following commands:

            * ``docker stop dxlelasticsearchservice``
            * ``docker restart dxlelasticsearchservice``
            * ``docker start dxlelasticsearchservice``
