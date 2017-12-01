Basic Update Example
====================

This sample updates a document to an Elasticsearch server via the Elasticsearch
``Update`` API. The sample then retrieves the contents of the updated document
via a call to the Elasticsearch ``Get`` API. The sample displays the results of
the ``Update`` and ``Get`` calls.

For more information on the Elasticsearch ``Update`` API, see the
`Elasticsearch Python Update API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.update>`__
and `Elasticsearch REST Update API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html>`__
documentation.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`).
* The Elasticsearch API DXL service is running, using the ``sample``
  configuration (see :doc:`running`).
* Run through the steps in the :doc:`basicindexexample`
  to store a document to Elasticsearch. This example will update a portion of
  the stored document.

Running
*******

To run this sample execute the ``sample/basic/basic_update_example.py`` script
as follows:

    .. code-block:: shell

        python sample/basic/basic_update_example.py

If the document was previously stored via running the :doc:`basicindexexample`,
the output should appear similar to the following:

    .. code-block:: shell

        Response to the update request:
        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-service-examples",
            "_shards": {
                "failed": 0,
                "successful": 2,
                "total": 2
            },
            "_type": "basic-example-doc",
            "_version": 2,
            "result": "updated"
        }
        Response to the get request:
        {
            "_id": "12345",
            "_index": "opendxl-elasticsearch-service-examples",
            "_source": {
                "message": "Hello from OpenDXL",
                "source": "Basic Update Example"
            },
            "_type": "basic-example-doc",
            "_version": 2,
            "found": true
        }

If the document to be updated does not exist at the time the sample is run,
the output should appear similar to the following:

    .. code-block:: shell

        Error invoking service with topic '/opendxl-elasticsearch/service/elasticsearch-api/update': TransportError(404, u'document_missing_exception', u'[basic-example-doc][12345]: document missing') (0)
        Error payload:
        {
            "class": "NotFoundError",
            "data": {
                "error": "document_missing_exception",
                "info": {
                    "error": {
                        "index": "opendxl-elasticsearch-service-examples",
                        "index_uuid": "f1Zn6yLMQcSTyclOwuprlA",
                        "reason": "[basic-example-doc][12345]: document missing",
                        "root_cause": [
                            {
                                "index": "opendxl-elasticsearch-service-examples",
                                "index_uuid": "f1Zn6yLMQcSTyclOwuprlA",
                                "reason": "[basic-example-doc][12345]: document missing",
                                "shard": "4",
                                "type": "document_missing_exception"
                            }
                        ],
                        "shard": "4",
                        "type": "document_missing_exception"
                    },
                    "status": 404
                },
                "status_code": 404
            },
            "module": "elasticsearch.exceptions"
        }

Details
*******

In order to enable the use of the ``update`` and ``get`` APIs, both API names
are listed in the ``apiNames`` setting under the ``[General]`` section in the
``sample`` "dxlelasticsearchservice.config" file that the service uses:

    .. code-block:: ini

        [General]
        apiNames=...,get,update,...

For more information on the configuration, see the
:ref:`Service Configuration File <dxl_service_config_file_label>` section.

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            logger.info("Connected to DXL fabric.")

            # Create the update request
            request_topic = "/opendxl-elasticsearch/service/elasticsearch-api/update"
            update_request = Request(request_topic)

            # Set the payload for the update request
            MessageUtils.dict_to_json_payload(update_request, {
                "index": DOCUMENT_INDEX,
                "doc_type": DOCUMENT_TYPE,
                "id": DOCUMENT_ID,
                "body": {
                    "doc": {
                        "source": "Basic Update Example"}}})

            # Send the update request
            update_response = client.sync_request(update_request, timeout=30)

            if update_response.message_type != Message.MESSAGE_TYPE_ERROR:
                # Display results for the update request
                update_response_dict = MessageUtils.json_payload_to_dict(
                    update_response)
                print("Response to the update request:\n{}".format(
                    MessageUtils.dict_to_json(update_response_dict,
                                              pretty_print=True)))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, update_response.error_message,
                    update_response.error_code))
                if update_response.payload:
                    # Display the payload in the error response
                    res_dict = MessageUtils.json_payload_to_dict(update_response)
                    print("Error payload:\n{}".format(
                        MessageUtils.dict_to_json(res_dict, pretty_print=True)))
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
that targets the "update" method of the Elasticsearch API DXL service.

The next step is to set the ``payload`` of the request message. The contents of
the payload include the ``index``, type (``doc_type``), and ``id`` of the
document to update. The contents also include a ``dict`` representing the
portion of the document ``body`` to update.

From the
`Elasticsearch Python Update API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.update>`_
documentation:

    `"Update a document based on a script or partial data provided."`

The next step is to perform a synchronous request via the DXL fabric. If the
response message is not an error, its contents are displayed.

To confirm that the document was updated properly, a second request message is
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
