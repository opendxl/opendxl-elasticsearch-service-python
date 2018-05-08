Basic Domain Suggestions Example
================================

This sample invokes and displays the results of a DomainTools "Domain Suggestions" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/domain-suggestions/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_domain_suggestions_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_domain_suggestions_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "query": "domain tools",
                "status_codes": {
                    "d": "deleted and available again",
                    "e": "on-hold (pending delete)",
                    "g": "on-hold (redemption period)",
                    "h": "on-hold (generic)",
                    "p": "registered and parked or redirected",
                    "q": "never registered before",
                    "w": "registered and active website",
                    "x": "registered and no website"
                },
                "suggestions": [
                    {
                        "domain": "domainfreetools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainusatools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainbuytools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainnetworktools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domaingametools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domaincheaptools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainblogtools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainsupporttools",
                        "status": "wqqqqq"
                    },
                    {
                        "domain": "domainhelptools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domaincoachtools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainrecoverytools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainseotools",
                        "status": "wqqqqq"
                    },
                    {
                        "domain": "domainmanagertools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainwealthtools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainestatetools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domaindesigntools",
                        "status": "qqqqqq"
                    },
                    {
                        "domain": "domainsecuritytools",
                        "status": "qqqqqq"
                    },
                    ...
                ],
                "tlds": [
                    "COM",
                    "NET",
                    "ORG",
                    "INFO",
                    "BIZ",
                    "US"
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

            request_topic = "/opendxl-domaintools/service/domaintools/domain_suggestions"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domain tools"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "domain suggestions" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Domain Suggestions Documentation <https://www.domaintools.com/resources/api-documentation/domain-suggestions/>`_:

    `"The Domain Suggestions API provides a list of domain names that are similar to the words in a query string. It has a bias
    toward available domains and provides suggestions for .com, .net, .org, .info, .biz, and .us top level domain names."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.
