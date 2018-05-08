Basic Domain Profile Example
============================

This sample invokes and displays the results of a DomainTools "Domain Profile" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/domain-profile/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_domain_profile_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_domain_profile_example.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "history": {
                    "ip_address": {
                        "events": 91,
                        "product_url": "https://research.domaintools.com/research/hosting-history/?q=domaintools.com",

                        "timespan_in_years": 11
                    },
                    "name_server": {
                        "events": 6,
                        "product_url": "https://research.domaintools.com/research/hosting-history/?q=domaintools.com",

                        "timespan_in_years": 9
                    },
                    "registrar": {
                        "earliest_event": "2002-04-12",
                        "events": 4,
                        "product_url": "https://research.domaintools.com/research/hosting-history/?q=domaintools.com"
                    },
                    "whois": {
                        "earliest_event": "2001-10-26",
                        "product_url": "https://research.domaintools.com/research/whois-history/search/?q=domaintools.
        com",
                        "records": 4197
                    }
                },
                "name_servers": [
                    {
                        "product_url": "https://reversens.domaintools.com/search/?q=NS1.P09.DYNECT.NET",
                        "server": "NS1.P09.DYNECT.NET"
                    },
                    {
                        "product_url": "https://reversens.domaintools.com/search/?q=NS2.P09.DYNECT.NET",
                        "server": "NS2.P09.DYNECT.NET"
                    },
                    {
                        "product_url": "https://reversens.domaintools.com/search/?q=NS3.P09.DYNECT.NET",
                        "server": "NS3.P09.DYNECT.NET"
                    },
                    {
                        "product_url": "https://reversens.domaintools.com/search/?q=NS4.P09.DYNECT.NET",
                        "server": "NS4.P09.DYNECT.NET"
                    }
                ],
                "registrant": {
                    "domains": 271,
                    "name": "DOMAINTOOLS, LLC",
                    "product_url": "https://reversewhois.domaintools.com/?all[]=DOMAINTOOLS%2C+LLC&none[]="
                },
                "registration": {
                    "created": "1998-08-02",
                    "expires": "2018-08-01",
                    "registrar": "ENOM, INC.",
                    "statuses": [
                        "clientTransferProhibited"
                    ],
                    "updated": "2017-07-03"
                },
                "seo": {
                    "product_url": "https://research.domaintools.com/seo-browser/?domain=domaintools.com",
                    "score": 75
                },
                "server": {
                    "ip_address": "199.30.228.112",
                    "other_domains": 3,
                    "product_url": "https://reverseip.domaintools.com/search/?q=domaintools.com"
                },
                "website_data": {
                    "meta": [],
                    "product_url": "https://whois.domaintools.com/domaintools.com",
                    "response_code": 200,
                    "server": "Here and There",
                    "title": "Home | DomainTools"
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

            request_topic = "/opendxl-domaintools/service/domaintools/domain_profile"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools.com"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))

After connecting to the DXL fabric, a `request message` is created with a topic that targets the "domain profile" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Domain Profile Documentation <https://www.domaintools.com/resources/api-documentation/domain-profile/>`_:

    `"The Domain Profile API provides basic domain name registration details and a preview of additional data available from DomainTools
    membership and report products. The preview data is especially useful for DomainTools affiliates who want to show useful information
    on a domain name or a registrant in their affiliate link."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.
