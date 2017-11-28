Basic Index Example
===================

This sample stores a document to an Elasticsearch server via the Elasticsearch
``Index`` API. The sample then retrieves the contents of the stored document
via a call to the Elasticsearch ``Get`` API. The sample displays the results of
the ``Index`` and ``Get`` calls.

For more information on the Elasticsearch ``Index`` API, see the
`Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`__
and `Elasticsearch REST Index API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html>`__
documentation.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`).
* The Elasticsearch API DXL service is running, using the ``sample``
  configuration (see :doc:`running`).

Running
*******

To run this sample execute the ``sample/basic/basic_index_example.py`` script
as follows:

    .. code-block:: shell

        python sample/basic/basic_index_example.py

The output should appear similar to the following:

    .. code-block:: shell

        Response to the index request:
        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-service-examples",
            "_shards": {
                "failed": 0,
                "successful": 2,
                "total": 2
            },
            "_type": "basic-example-doc",
            "_version": 1,
            "created": true,
            "result": "created"
        }
        Response to the get request:
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

Details
*******

In order to enable the use of the ``index`` and ``get`` APIs, both API names
are listed in the ``apiNames`` setting under the ``[General]`` section in the
``sample`` "dxlelasticsearchservice.config" file that the service uses:

    .. code-block:: ini

        [General]
        apiNames=index,get...

For more information on the configuration, see the
:ref:`Service Configuration File <dxl_service_config_file_label>` section.

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            logger.info("Connected to DXL fabric.")

            # Create the index request
            request_topic = "/opendxl-elasticsearch/service/elasticsearch-api/index"
            index_request = Request(request_topic)

            # Set the payload for the index request
            MessageUtils.dict_to_json_payload(index_request, {
                "index": DOCUMENT_INDEX,
                "doc_type": DOCUMENT_TYPE,
                "id": DOCUMENT_ID,
                "body": {
                    "message": "Hello from OpenDXL",
                    "source": "Basic Index Example"}})

            # Send the index request
            index_response = client.sync_request(index_request, timeout=30)

            if index_response.message_type != Message.MESSAGE_TYPE_ERROR:
                # Display results for the index request
                index_response_dict = MessageUtils.json_payload_to_dict(index_response)
                print("Response to the index request:\n{}".format(
                    MessageUtils.dict_to_json(index_response_dict, pretty_print=True)))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, index_response.error_message,
                    index_response.error_code))
                exit(1)

            # Create the get request
            request_topic = "/opendxl-elasticsearch/service/elasticsearch-api/get"
            get_request = Request(request_topic)

            # Set the payload for the get request
            MessageUtils.dict_to_json_payload(get_request, {
                "index": DOCUMENT_INDEX,
                "doc_type": DOCUMENT_TYPE,
                "id": DOCUMENT_ID})

            # Send the get request
            get_response = client.sync_request(get_request, timeout=30)

            if get_response.message_type != Message.MESSAGE_TYPE_ERROR:
                # Display results for the get request
                get_response_dict = MessageUtils.json_payload_to_dict(get_response)
                print("Response to the get request:\n{}".format(
                    MessageUtils.dict_to_json(get_response_dict, pretty_print=True)))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, get_response.error_message,
                    get_response.error_code))


After connecting to the DXL fabric, a request message is created with a topic
that targets the "index" method of the Elasticsearch API DXL service.

The next step is to set the ``payload`` of the request message. The contents of
the payload include the ``index``, type (``doc_type``), and ``id`` at which to
store the document. The contents also include a ``dict`` representing the
``body`` of the document to store.

From the
`Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`_
documentation:

    `"Adds or updates a typed JSON document in a specific index, making it
    searchable."`

The next step is to perform a synchronous request via the DXL fabric. If the
response message is not an error, its contents are displayed.

To confirm that the document was stored properly, a second request message is
created with a topic that targets the "get" method of the Elasticsearch API DXL
service.

The next step is to set the ``payload`` of the request message. The contents of
the payload include the ``index``, type (``doc_type``), and ``id`` of the
document to retrieve.

From the
`Elasticsearch Python Get API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.get>`_
documentation:

    `"Get a typed JSON document from the index based on its id."`

The next step is to perform a synchronous request via the DXL fabric. If the
response message is not an error, its contents are displayed.
