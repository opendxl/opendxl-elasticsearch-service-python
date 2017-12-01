Basic Event Example
===================

This sample sends an event to a DXL broker. The DXL Elasticsearch service
receives a notification for the event and stores the payload into a document
on an Elasticsearch server. The sample then retrieves the contents of the stored document
via a call to the Elasticsearch ``Get`` API. The sample displays the results of
the ``Get`` call.

For more information on the Elasticsearch ``Get`` API, see the
`Elasticsearch Python Get API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.get>`__
and `Elasticsearch REST Get API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html>`__
documentation.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`).
* The Elasticsearch API DXL service is running, using the ``sample``
  configuration (see :doc:`running`).

Running
*******

To run this sample execute the ``sample/basic/basic_event_example.py`` script
as follows:

    .. code-block:: shell

        python sample/basic/basic_event_example.py

The output should appear similar to the following:

    .. code-block:: shell

        Waiting for event payload to be stored in Elasticsearch...
        Response to the get request:
        {
            "_id": "basic-event-example-id",
            "_index": "opendxl-elasticsearch-service-examples",
            "_source": {
                "event_id": "basic-event-example-id",
                "message": "Hello from OpenDXL",
                "source": "Basic Event Example"
            },
            "_type": "basic-event-example-doc",
            "_version": 1,
            "found": true
        }

Details
*******

In order to enable the use of the ``get`` API, the API name is listed in the
``apiNames`` setting under the ``[General]`` section in the ``sample``
"dxlelasticsearchservice.config" file that the service uses:

    .. code-block:: ini

        [General]
        apiNames=...,get,...

The "dxlelasticsearchservice.config" file also includes some settings which
instruct the service to store the event payload into an Elasticsearch document:

    .. code-block:: ini

        [General]
        eventGroupNames=basic_event_example,...

        [basic_event_example]
        topics=/sample/elasticsearch/basicevent
        documentIndex=opendxl-elasticsearch-service-examples
        documentType=basic-event-example-doc
        idFieldName=event_id

The ``basic_event_example`` event group section lists the name of the event
topic which the sample sends, ``/sample/elasticsearch/basicevent``. The payload
for each matching event received is stored into Elasticsearch as a document
with the index (``documentIndex``) and type (``documentType``) listed in the
configuration. The ID for the Elasticsearch document is retrieved from the
field name in the event payload which corresponds to the value for the
``idFieldName`` setting, ``event_id``. The sample includes the following
payload for the event:

    .. code-block:: json

        {
            "event_id": "basic-event-example-id",
            "message": "Hello from OpenDXL",
            "source": "Basic Event Example"
        }

Since the value in the payload for the ``event_id`` field is
``basic-event-example-id``, the ID of the document stored to Elasticsearch for
the event is also ``basic-event-example-id``.

For more information on the configuration, see the
:ref:`Service Configuration File <dxl_service_config_file_label>` section.

For more information on the Elasticsearch document storage process, see the
`Elasticsearch REST Index API <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html>`__.

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            logger.info("Connected to DXL fabric.")

            # Create the event
            event = Event(EVENT_TOPIC)

            # Set the payload
            MessageUtils.dict_to_json_payload(event, {
                "event_id": DOCUMENT_ID,
                "message": "Hello from OpenDXL",
                "source": "Basic Event Example"})

            # Send the event
            client.send_event(event)

            # Create the get request
            request_topic = "/opendxl-elasticsearch/service/elasticsearch-api/get"
            req = Request(request_topic)

            # Set the payload for the get request
            MessageUtils.dict_to_json_payload(req, {
                "index": DOCUMENT_INDEX,
                "doc_type": DOCUMENT_TYPE,
                "id": DOCUMENT_ID})

            print("Waiting for event payload to be stored in Elasticsearch...")
            time.sleep(5)

            # Send a request to the elasticsearch DXL service to retrieve the document
            # that should be stored for the event.
            res = client.sync_request(req, timeout=30)

            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                # Display results for the get request
                res_dict = MessageUtils.json_payload_to_dict(res)
                print("Response to the get request:\n{}".format(
                    MessageUtils.dict_to_json(res_dict, pretty_print=True)))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))
                if res.payload:
                    # Display the payload in the error response
                    res_dict = MessageUtils.json_payload_to_dict(res)
                    print("Error payload:\n{}".format(
                        MessageUtils.dict_to_json(res_dict, pretty_print=True)))


After connecting to the DXL fabric, an event is sent to the fabric.

Upon receipt of a notification for the event, the DXL Elasticsearch service
stores a corresponding document to the Elasticsearch server.

To confirm that the document was stored properly, a request message is created
with a topic that targets the "get" method of the Elasticsearch API DXL
service.

The next step is to set the ``payload`` of the request message. The contents of
the payload include the ``index``, type (``doc_type``), and ``id`` of the
document to retrieve.

From the
`Elasticsearch Python Get API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.get>`_
documentation:

    `"Get a typed JSON document from the index based on its id."`

The next step is to perform a synchronous request via the DXL fabric. Since the
process of storing the document to Elasticsearch is asynchronous to sending
the event, the "get" requests are repeated up to 5 times, with a delay of 2
seconds between requests, to allow some time for the document to be stored
before it can be retrieved. If the result after retries in getting the stored
document is not an error, the response from the successful "get" request is
displayed.
