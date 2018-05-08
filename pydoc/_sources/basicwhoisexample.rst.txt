Basic Whois Lookup Example
==========================

This sample invokes and displays the results of a DomainTools "Whois Lookup" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/whois-lookup/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_whois_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_whois_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "name_servers": [
                    "NS1.P09.DYNECT.NET",
                    "NS2.P09.DYNECT.NET",
                    "NS3.P09.DYNECT.NET",
                    "NS4.P09.DYNECT.NET"
                ],
                "record_source": "domaintools.com",
                "registrant": "DOMAINTOOLS, LLC",
                "registration": {
                    "created": "1998-08-02",
                    "expires": "2018-08-01",
                    "registrar": "ENOM, INC.",
                    "statuses": [
                        "clientTransferProhibited"
                    ],
                    "updated": "2017-07-03"
                },
                "whois": {
                    "date": "2017-07-17",
                    "record": "Domain Name: DOMAINTOOLS.COM\nRegistry Domain ID: 1697312_DOMAIN_COM-VRSN\nRegistrar"
                    "...."
                }
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

            request_topic = "/opendxl-domaintools/service/domaintools/whois"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools.com"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "whois" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Whois Lookup Documentation <https://www.domaintools.com/resources/api-documentation/whois-lookup/>`_:

    `"The Whois Lookup API provides the ownership record for a domain name or IP address with basic registration details."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

