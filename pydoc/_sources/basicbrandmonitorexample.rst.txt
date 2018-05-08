Basic Brand Monitor Example
===========================

This sample invokes and displays the results of a DomainTools "Brand Monitor" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/brand-monitor/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_brand_monitor_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_brand_monitor_example.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "alerts": [],
                "date": "2017-07-17",
                "exclude": [],
                "limit": 3000,
                "new": true,
                "on-hold": true,
                "query": "domaintools",
                "total": 0,
                "utf8": false
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

            request_topic = "/opendxl-domaintools/service/domaintools/brand_monitor"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))

After connecting to the DXL fabric, a `request message` is created with a topic that targets the "brand monitor" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Brand Monitor Documentation <https://www.domaintools.com/resources/api-documentation/brand-monitor/>`_:

    `"The Brand Monitor API will search across all new domain registrations worldwide, and return result sets consisting of domain names
    that contain a customer's brand or monitored word/string. The Brand Monitor API looks at country code TLDS and new generic TLDs,
    as well as the usual suspects of .COM, .NET,.ORG, etc."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

