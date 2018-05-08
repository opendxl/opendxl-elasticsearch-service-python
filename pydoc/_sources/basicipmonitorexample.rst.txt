Basic IP Monitor Example
========================

This sample invokes and displays the results of a DomainTools "IP Monitor" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/ip-monitor/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_ip_monitor_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_ip_monitor_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "alerts": [],
                "date": "2017-07-18",
                "ip_address": "65.55.53.233",
                "limit": 1000,
                "page": 1,
                "page_count": 0,
                "total": "0"
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

            request_topic = "/opendxl-domaintools/service/domaintools/ip_monitor"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "65.55.53.233"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "ip monitor" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `IP Monitor Documentation <https://www.domaintools.com/resources/api-documentation/ip-monitor/>`_:

    `"The IP Monitor API searches the daily activity of all our monitored TLDs on any given IP address. New, Deleted and
    Transferred domains records can be queried up to 6 days in the past."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

