Basic Reputation Example
========================

This sample invokes and displays the results of a DomainTools "Reputation" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/reputation/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_reputation_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_reputation_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "domain": "domaintools.com",
                "risk_score": 0
            }
        }

The received results are displayed.

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:
            # Connect to the fabric
            client.connect()

            logger.info("Connected to DXL fabric.")

            request_topic = "/opendxl-domaintools/service/domaintools/reputation"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools.com"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "reputation" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Reputation Documentation <https://www.domaintools.com/resources/api-documentation/reputation/>`_:

    `"Provides a risk score for the domain.
    The Reputation API is only available via our Enterprise Solutions team, and is not included in a membership."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

