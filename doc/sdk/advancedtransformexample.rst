Advanced Transform Example
==========================

This sample, similar to the :doc:`basiceventexample`, sends an event to a DXL
broker. The DXL Elasticsearch service receives a notification for the event and
stores the payload into documents on an Elasticsearch server. The sample then
retrieves the contents of the stored documents via a call to the Elasticsearch
``Get`` API. The sample displays the results of the ``Get`` call.

The most significant difference between the behavior for this sample and the
:doc:`basiceventexample` is that this sample configures a custom Python script
which the Elasticsearch service invokes to transform the content of the event
payload. The transform script defines two separate Elasticsearch documents
which are stored for the event.

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

To run this sample execute the ``sample/basic/advanced_transform_example.py``
script as follows:

    .. code-block:: shell

        python sample/basic/advanced_transform_example.py

The output should appear similar to the following:

    .. code-block:: shell

        Waiting for event payloads to be stored in Elasticsearch...
        Response to the get request for id 'advanced-event-example-id-1':
        {
            "_id": "advanced-event-example-id-1",
            "_index": "opendxl-elasticsearch-service-examples",
            "_source": {
                "id": "advanced-event-example-id-1",
                "message": "Hello from OpenDXL",
                "source": "Advanced Transform Example"
            },
            "_type": "advanced-transform-example-doc",
            "_version": 1,
            "found": true
        }
        Response to the get request for id 'advanced-event-example-id-2':
        {
            "_id": "advanced-event-example-id-2",
            "_index": "opendxl-elasticsearch-service-examples",
            "_source": {
                "id": "advanced-event-example-id-2",
                "message": "Hello from OpenDXL",
                "source": "Advanced Transform Example"
            },
            "_type": "advanced-transform-example-doc",
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
        eventGroupNames=...,advanced_transform_example

        [advanced_transform_example]
        topics=/sample/elasticsearch/advancedtransform
        documentIndex=opendxl-elasticsearch-service-examples
        documentType=advanced-transform-example-doc
        transformScript=advanced_transform_example_script.py

The ``advanced_transform_example`` event group section lists the name of the
event topic which the sample sends,
``/sample/elasticsearch/advancedtransform``. The payload for each matching
event received is passed into an ``on_event`` function defined by the
``advanced_transform_example_script.py`` script. The ``on_event`` function
transforms the event payload into parameters for two corresponding documents
which are stored to the Elasticsearch server. See the code snippets below for
more information on the transform script.

For more information on the configuration, see the
:ref:`Service Configuration File <dxl_service_config_file_label>` section.

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
            MessageUtils.encode_payload(event, "Hello from OpenDXL")

            # Send the event
            client.send_event(event)

            print("Waiting for event payloads to be stored in Elasticsearch...")
            time.sleep(5)

            for document_id in DOCUMENT_IDS:
                # Create the get request
                request_topic = "/opendxl-elasticsearch/service/elasticsearch-api/get"
                req = Request(request_topic)

                # Set the payload for the get request
                MessageUtils.dict_to_json_payload(req, {
                    "index": DOCUMENT_INDEX,
                    "doc_type": DOCUMENT_TYPE,
                    "id": document_id})

               # Send a request to the elasticsearch DXL service to try to retrieve the
               # document that should be stored for the event.
                res = client.sync_request(req, timeout=30)

                if res.message_type != Message.MESSAGE_TYPE_ERROR:
                    # Display results for the get request
                    res_dict = MessageUtils.json_payload_to_dict(res)
                    print("Response to the get request for id '{}':\n{}".format(
                        document_id,
                        MessageUtils.dict_to_json(res_dict, pretty_print=True)))
                else:
                    print("Error invoking service with topic '{}' for id '{}': {} ({})".format(
                        request_topic, document_id, res.error_message, res.error_code))
                    if res.payload:
                        # Display the payload in the error response
                        res_dict = MessageUtils.json_payload_to_dict(res)
                        print("Error payload:\n{}".format(
                            MessageUtils.dict_to_json(res_dict, pretty_print=True)))


After connecting to the DXL fabric, an event is sent to the fabric.

Upon receipt of a notification for the event, the DXL Elasticsearch service
passes the event information along to the ``on_event`` function in the
transform script configured for the event group. The script is named
``advanced_transform_example_script.py`` and resides the ``sample`` directory.
The majority of the code for the ``advanced_transform_example_script.py``
script is below:

    .. code-block:: python

        def on_event(event, index_operation):
            """
            Callback invoked with content received for a DXL event. The callback should
            return a dictionary (or list of dictionaries) with parameters for the
            Elasticsearch index operation(s) that the service should perform.

            The elements for each dictionary returned should correspond to parameters
            in the `Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`__.
            For example, the value for the "doc_type" element in the dictionary will be
            supplied as the "doc_type" parameter for the Elasticsearch "index"
            operation.

            :param dxlclient.message.Event event: The event which was received.
            :param dict index_operation: A dict with a set of parameters configured
                for storing the event payload into Elasticsearch. The dictionary
                should include the following:

                .. code-block::python

                { "index": "<documentIndex value from the application config>",
                  "doc_type": "<documentType value from the application config>",
                  "body": "<payload from the event parameter>",
                  "id": "<id from event payload>" }

            If the event payload could be converted into a dict from JSON, the
            value for the "body" element will be a dict. Otherwise, the payload
            will be a str.

            The value for the "id" element is pulled from the value for the key
            in the event payload which corresponds to the "idFieldName" value
            in the application configuration. If no value was set for "idFieldName"
            in the application configuration, the value for the "id" element is
            None.

            :return: A dictionary (or list of dictionaries) with parameters for an
                Elasticsearch "index" operation to perform. If None is returned, no
                "index" operations will be performed.
            :rtype: dict or list(dict)
            """
            logger.info("Event payload received for transform: %s", event.payload)
            logger.info("Index operation received for transform: %s", index_operation)

            # Modify the "id" and "body" elements in the index operation dictionary.
            event_payload = MessageUtils.decode_payload(event)
            index_operation["id"] = "advanced-event-example-id-1"
            # Store the event payload string in a dictionary. This allows Elasticsearch
            # to serialize the document into JSON for storage.
            index_operation["body"] = MessageUtils.dict_to_json({
                "id": index_operation["id"],
                "message": event_payload,
                "source": "Advanced Transform Example"})

            # Create a second index operation dictionary, using some of the values
            # from the first dictionary.
            another_index_operation = {
                "index": index_operation["index"],
                "doc_type": index_operation["doc_type"],
                "id": "advanced-event-example-id-2",
                "body": MessageUtils.dict_to_json({
                    "id": "advanced-event-example-id-2",
                    "message": event_payload,
                    "source": "Advanced Transform Example"})
            }

            # Return info for two documents to store in Elasticsearch.
            return [index_operation, another_index_operation]


The first parameter to the ``on_event`` function (``event``) contains the
``dxlclient.message.Event`` object which was received for the event
notification. The second parameter to the function (``index_operation``)
contains a ``dict`` with elements which map to parameters in the `Elasticsearch
Python Index API
<https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`__.
The elements in the ``dict`` are preconfigured with information from the event
received from the DXL fabric:

    .. code-block:: python

        {
            "index": "opendxl-elasticsearch-service-examples",
            "doc_type": "advanced-transform-example-doc",
            "id": None,
            "body": "Hello from OpenDXL"
        }

The ``on_event`` function fills out and returns parameters for two different
documents to be stored to Elasticsearch:

1) For the first index operation ``dict``, the function modifies the
   ``index_operation`` input parameter with a value for the document ``id`` and
   ``body``.

2) For the second index operation ``dict``, the function copies over some of
   the values from the ``index_operation`` input parameter.

The DXL Elasticsearch service uses the Elasticsearch ``Index`` API to store the
index operation dictionaries to Elasticsearch. For more information on the
parameters which can be set for an index operation, see the
`Elasticsearch Python Index API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index>`__
documentation.

To confirm that that the two documents were stored properly, the sample creates
a request message with a topic that targets the "get" method of the
Elasticsearch API DXL service.

The next step is to set the ``payload`` of the request message. The contents of
the payload include the ``index``, type (``doc_type``), and ``id`` of the
document to retrieve.

From the
`Elasticsearch Python Get API <https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.get>`_
documentation:

    `"Get a typed JSON document from the index based on its id."`

The next step is to perform a synchronous request via the DXL fabric. Since the
process of storing the documents to Elasticsearch is asynchronous to sending
the event, the "get" requests are repeated up to 5 times, with a delay of 2
seconds between requests, to allow some time for the documents to be stored
before they can be retrieved. If the result after retries in getting each
stored document is not an error, the response from the successful "get" request
is displayed. The request process is performed twice, once for each document
defined by the transform script which is expected to be stored to
Elasticsearch.
