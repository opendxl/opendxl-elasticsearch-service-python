Basic PhishEye Example
======================

This sample invokes and displays the results of a DomainTools "PhishEye" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/phisheye/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_phisheye_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_phisheye_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
              "term": "apple",
              "date": "2016-11-01",
              "domains": [
                {
                  "domain" : "firstexample-apple.com",
                  "tld": "com",
                  "created_date": "2016-10-30",
                  "registrant_email": "somebody@example.com",
                  "name_servers": [
                    "ns1.example.com",
                    "ns2.example.com"
                  ],
                  "registrar_name": "Some Registrar 1",
                  "risk_score": 88
                },
                {
                  "domain": "appeltypoexample.com",
                  "tld": "com",
                  "created_date": "2016-10-31",
                  "registrant_email": "somebody2@example.com",
                  "ip_addresses": [
                    {
                      "ip": "192.0.2.100",
                      "country_code": "US"
                    },
                    {
                      "ip": "192.0.2.101",
                      "country_code": "US"
                    }
                  ],
                  "name_servers": [
                    "ns57.domaincontrol.com",
                    "ns58.domaincontrol.com"
                  ],
                  "registrar_name": "GoDaddy.com, LLC",
                  "risk_score": 24
                },
                {
                  "domain": "thirdexample-apple.ru",
                  "tld": "ru",
                  "created_date": "2014-09-23",
                  "registrant_email": "somebody3@example.com",
                  "registrar_name": "1API GmbH",
                  "risk_score": 33
                },
                ...
              ]
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

            request_topic = "/opendxl-domaintools/service/domaintools/phisheye"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "apple"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))

After connecting to the DXL fabric, a `request message` is created with a topic that targets the "phisheye" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `PhishEye Documentation <https://www.domaintools.com/resources/api-documentation/phisheye/>`_:

    `"The PhishEye API provides programmatic access to daily monitor results from the DomainTools PhishEye product.
    The PhishEye API is only available via our Enterprise Solutions team, and is not included in a membership."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

