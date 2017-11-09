Service Methods
===============

To make an Elasticsearch API method available to the DXL fabric, the method
name should be added to the ``apiNames`` setting in the ``[General]`` section
of the :ref:`Service Configuration File <dxl_service_config_file_label>`. The
service registers a DXL request topic for each valid API name listed in the
configuration file. A JSON document with the names and values for each API
parameter should be provided with requests made for the DXL topic.

For example, to make a request to the Elasticsearch ``get`` API method, the
following steps could be taken:

1) Add ``get`` to the list of ``apiNames`` in the configuration file:

    .. code-block:: ini

        [General]
        apiNames=get,...

2) (Re)start the DXL Elasticsearch service.

    The service should register the following request topic on the DXL fabric:

     **/opendxl-elasticsearch/service/elasticsearch-api/get**

3) Send a request for the DXL topic with a JSON payload which contains the
   desired parameters, for example:

    .. code-block:: json

        {
            "index": "opendxl-elasticsearch-service-examples",
            "doc_type": "basic-example-doc",
            "id": "12345"
        }

    The service should respond with the contents of the stored document, for
    example:

    .. code-block:: json

        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-service-examples",
            "_source": {
                "message": "Hello from OpenDXL",
                "source": "Basic Index Example"
            },
            "_type": "basic-example-doc",
            "_version": 1,
            "found": true
        }

The Elasticsearch DXL Python service APIs are basically just thin wrappers on
top of the underlying client APIs used in the
`elasticsearch-py <https://github.com/elastic/elasticsearch-py>`_ Python
library. For a complete list of the available API method names and parameters,
see the
`Elasticsearch client API documentation <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch>`_.
