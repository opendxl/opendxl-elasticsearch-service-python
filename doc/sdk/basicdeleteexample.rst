Basic Delete Example
====================

This sample deletes a document from an Elasticsearch server via the
Elasticsearch ``Delete`` API and displays the results of the delete request.

For more information on the Elasticsearch ``Delete`` API, see the
`Elasticsearch Python Delete API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.delete>`__
and `Elasticsearch REST Delete API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html>`__
documentation.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`).
* The Elasticsearch API DXL service is running, using the ``sample``
  configuration (see :doc:`running`).
* Run through the steps in the :doc:`basicindexexample`
  to store a document to Elasticsearch. This example will delete the stored
  document.

Running
*******

To run this sample execute the ``sample/basic/basic_delete_example.py`` script
as follows:

    .. code-block:: shell

        python sample/basic/basic_delete_example.py

If the document was previously stored via running the :doc:`basicindexexample`,
the output should appear similar to the following:

    .. code-block:: shell

        Response to the delete request:
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
            "found": true,
            "result": "deleted"
        }

If the document to be deleted does not exist at the time the sample is run,
the output should appear similar to the following:

    .. code-block:: shell

        Error invoking service with topic '/opendxl-elasticsearch/service/elasticsearch-api/delete': TransportError(404, u'{"found":false,"_index":"opendxl-elasticsearch-service-examples","_type":"basic-example-doc","_id":"12345","_version":3,"result":"not_found","_shards":{"total":2,"successful":2,"failed":0}}') (0)
        Error payload:
        {
            "class": "NotFoundError",
            "data": {
                "error": "{\"found\":false,\"_index\":\"opendxl-elasticsearch-service-examples\",\"_type\":\"basic-example-doc\",\"_id\":\"123
        45\",\"_version\":3,\"result\":\"not_found\",\"_shards\":{\"total\":2,\"successful\":2,\"failed\":0}}",
                "info": {
                    "_id": "12345",
                    "_index": "opendxl-elasticsearch-service-examples",
                    "_shards": {
                        "failed": 0,
                        "successful": 2,
                        "total": 2
                    },
                    "_type": "basic-example-doc",
                    "_version": 3,
                    "found": false,
                    "result": "not_found"
                },
                "status_code": 404
            },
            "module": "elasticsearch.exceptions"
        }

Details
*******

In order to enable the use of the ``delete`` API, the API name is listed in the
``apiNames`` setting under the ``[General]`` section in the ``sample``
"dxlelasticsearchservice.config" file that the service uses:

    .. code-block:: ini

        [General]
        apiNames=...,delete

For more information on the configuration, see the
:ref:`Service Configuration File <dxl_service_config_file_label>` section.

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            logger.info("Connected to DXL fabric.")

            # Create the delete request
            request_topic = "{}/delete".format(ELASTICSEARCH_API_TOPIC)
            req = Request(request_topic)

            # Set the payload for the delete request
            MessageUtils.dict_to_json_payload(req, {
                "index": DOCUMENT_INDEX,
                "doc_type": DOCUMENT_TYPE,
                "id": DOCUMENT_ID})

            # Send the delete request
            res = client.sync_request(req, timeout=30)

            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                # Display results for the delete request
                res_dict = MessageUtils.json_payload_to_dict(res)
                print("Response to the delete request:\n{}".format(
                    MessageUtils.dict_to_json(res_dict, pretty_print=True)))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))
                if res.payload:
                    # Display the payload in the error response
                    res_dict = MessageUtils.json_payload_to_dict(res)
                    print("Error payload:\n{}".format(
                        MessageUtils.dict_to_json(res_dict, pretty_print=True)))


After connecting to the DXL fabric, a request message is created with a topic
that targets the "delete" method of the Elasticsearch API DXL service.

The next step is to set the ``payload`` of the request message. The contents of
the payload include the ``index``, type (``doc_type``), and ``id`` of the
document to delete.

From the
`Elasticsearch Python Delete API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.delete>`_
documentation:

    `"Delete a typed JSON document from a specific index based on its id."`

The next step is to perform a synchronous request via the DXL fabric. If the
response message is not an error, its contents are displayed.
