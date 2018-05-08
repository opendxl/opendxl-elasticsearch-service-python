Basic Parsed Whois Example
==========================

This sample invokes and displays the results of a DomainTools "Parsed Whois" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/parsed-whois/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_parsed_whois_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_parsed_whois_example.py


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
                "parsed_whois": {
                    "contacts": {
                        "admin": {
                            "city": "SEATTLE",
                            "country": "US",
                            "email": "MEMBERSERVICES@DOMAINTOOLS.COM",
                            "fax": "12068389056",
                            "name": "DOMAIN ADMINISTRATOR",
                            "org": "DOMAINTOOLS, LLC",
                            "phone": "12068389035",
                            "postal": "98121",
                            "state": "WA",
                            "street": [
                                "2101 4TH AVE",
                                "SUITE 1150"
                            ]
                        },
                        "billing": {
                            "city": "",
                            "country": "",
                            "email": "",
                            "fax": "",
                            "name": "",
                            "org": "",
                            "phone": "",
                            "postal": "",
                            "state": "",
                            "street": []
                        },
                        "registrant": {
                            "city": "SEATTLE",
                            "country": "US",
                            "email": "MEMBERSERVICES@DOMAINTOOLS.COM",
                            "fax": "12068389056",
                            "name": "DOMAIN ADMINISTRATOR",
                            "org": "DOMAINTOOLS, LLC",
                            "phone": "12068389035",
                            "postal": "98121",
                            "state": "WA",
                            "street": [
                                "2101 4TH AVE",
                                "SUITE 1150"
                            ]
                        },
                        "tech": {
                            "city": "SEATTLE",
                            "country": "US",
                            "email": "MEMBERSERVICES@DOMAINTOOLS.COM",
                            "fax": "12068389056",
                            "name": "DOMAIN ADMINISTRATOR",
                            "org": "DOMAINTOOLS, LLC",
                            "phone": "12068389035",
                            "postal": "98121",
                            "state": "WA",
                            "street": [
                                "2101 4TH AVE",
                                "SUITE 1150"
                            ]
                        }
                    },
                    "created_date": "1998-08-02T04:00:00+00:00",
                    "domain": "domaintools.com",
                    "expired_date": "2018-08-01T04:00:00+00:00",
                    "name_servers": [
                        "ns1.p09.dynect.net",
                        "ns2.p09.dynect.net",
                        "ns3.p09.dynect.net",
                        "ns4.p09.dynect.net"
                    ],
                    "other_properties": {
                        "dnssec": "unSigned",
                        "registry_domain_id": "1697312_DOMAIN_COM-VRSN"
                    },
                    "registrar": {
                        "abuse_contact_email": "abuse@enom.com",
                        "abuse_contact_phone": "14252982646",
                        "iana_id": "48",
                        "name": "ENOM, INC.",
                        "url": "www.enom.com",
                        "whois_server": "whois.enom.com"
                    },
                    "statuses": [
                        "clientTransferProhibited https://www.icann.org/epp#clientTransferProhibited"
                    ],
                    "updated_date": "2017-07-03T00:43:03+00:00"
                },
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
                    "record": "Domain Name: DOMAINTOOLS.COM\nRegistry Domain ID: 1697312_DOMAIN_COM-VRSN\nRegistrar WHOIS Server:
                    whois.enom.com\nRegistrar URL: www.enom.com\nUpdated Date: 2017-07-03T00:43:03.00Z\nCreation
                    Date: 1998-08-02T04:00:00.00Z\nRegistrar Registration Expiration Date: 2018-08-01T04:00:00.00Z\nRegistrar:
                    ..."
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

            request_topic = "/opendxl-domaintools/service/domaintools/parsed_whois"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools.com"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "parsed whois" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Parsed Whois Documentation <https://www.domaintools.com/resources/api-documentation/parsed-whois/>`_:

    `"The Parsed Whois API provides parsed information extracted from the raw Whois record. The API is optimized to quickly
    retrieve the Whois record, group important data together and return a well-structured format. The Parsed Whois API is
    ideal for anyone wishing to search for, index, or cross-reference data from one or multiple Whois records."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

