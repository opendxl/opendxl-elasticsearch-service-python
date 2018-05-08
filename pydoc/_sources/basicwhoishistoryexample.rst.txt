Basic Whois History Example
===========================

This sample invokes and displays the results of a DomainTools "Whois History" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/whois-history/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_whois_history_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_whois_history_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "history": [
                    {
                        "date": "2001-10-26",
                        "is_private": 0,
                        "whois": {
                            "name_servers": [
                                "DNS1.INTERLAND.NET"
                            ],
                            "record": "Registrant:\nVRW2\n    7770 Regents Road #113/194\n    San Diego, CA 92122\n
                            ...",
                            "registrant": "VRW2",
                            "registration": {
                                "created": "1998-08-02",
                                "expires": "2002-08-02",
                                "registrar": "NETWORK SOLUTIONS, INC.",
                                "statuses": [
                                    "ACTIVE"
                                ]
                            }
                        }
                    },
                    {
                        "date": "2003-08-25",
                        "is_private": 0,
                        "whois": {
                            "name_servers": [
                                "NS1.XXXNAMESERVERS.COM"
                            ],
                            "record": "Registrant:\n DomainTools.com\n Taman Harapan 884\n Jakarta, XX 11040\n ID\n\n
                            ....",
                            "registrant": "DomainTools.com",
                            "registration": {
                                "created": "1998-08-02",
                                "expires": "2004-08-01",
                                "registrar": "TUCOWS, INC.",
                                "statuses": [
                                    "ACTIVE"
                                ]
                            }
                        }
                    },
                    ....
                ],
                "record_count": 46
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

            request_topic = "/opendxl-domaintools/service/domaintools/whois_history"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools.com"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "whois history" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Whois History Documentation <https://www.domaintools.com/resources/api-documentation/whois-history/>`_:

    `"The Whois History API provides a list of historic Whois records for a domain name."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

