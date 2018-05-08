Basic Registrant Monitor Example
================================

This sample invokes and displays the results of a DomainTools "Registrant Monitor" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/registrant-monitor/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_registrant_monitor_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_registrant_monitor_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "alerts": [],
                "date": "2017-07-18",
                "limit": 3000,
                "query": "domaintools",
                "total": 0
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

            request_topic = "/opendxl-domaintools/service/domaintools/registrant_monitor"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "registrant monitor" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Registrant Monitor Documentation <https://www.domaintools.com/resources/api-documentation/registrant-monitor/>`_:

    `"The Registrant Monitor API searches the ownership (Whois) records of domain names for specific search terms.
    The product is ideal for monitoring specific domain owners (such as "DomainTools LLC") to be alerted whenever their
    information appears in a newly-registered domain name."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

