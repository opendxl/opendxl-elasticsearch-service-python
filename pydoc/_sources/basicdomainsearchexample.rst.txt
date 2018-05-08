Basic Domain Search Example
===========================

This sample invokes and displays the results of a DomainTools "Domain Search" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/domain-search/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_domain_search_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_domain_search_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "query_info": {
                    "active_only": false,
                    "anchor_left": false,
                    "anchor_right": false,
                    "deleted_only": false,
                    "exclude_query": "",
                    "has_hyphen": true,
                    "has_number": true,
                    "limit": 100,
                    "max_length": 25,
                    "min_length": 1,
                    "page": 1,
                    "total_results": 510
                },
                "results": [
                    {
                        "char_count": 11,
                        "has_active": 1,
                        "has_deleted": 1,
                        "has_hyphen": 0,
                        "has_number": 0,
                        "hashad_tlds": [
                            "asia",
                            "at",
                            "be",
                            "biz",
                            "bz",
                            "ca",
                            "cc",
                            "cf",
                            "ch",
                            "cl",
                            "click",
                            "club",
                            "cm",
                            "cn",
                            "co",
                            "co.ba",
                            "co.il",
                            "horse",
                            "host",
                            "hu",
                            "xxx",
                            "xyz"
                        ],
                        "sld": "domaintools",
                        "tlds": [
                            "asia",
                            "at",
                            "be",
                            "biz",
                            "bz",
                            "ca",
                            "cc",
                            "cf",
                            "ch",
                            "space",
                            "store",
                            "support",
                            "sx",
                            "tech",
                            "technology",
                            "tel",
                            "tips",
                            "tk",
                            "tools",
                            "top",
                            "tv",
                            "tw",
                            "us",
                            "xxx",
                            "xyz"
                        ],
                        "tlds_count": 84
                    },
                    {
                        "char_count": 19,
                        "has_active": 1,
                        "has_deleted": 1,
                        "has_hyphen": 0,
                        "has_number": 0,
                        "hashad_tlds": [
                            "com"
                        ],
                        "sld": "domainbusinesstools",
                        "tlds": [
                            "com"
                        ],
                        "tlds_count": 1
                    },
                    ......
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

            request_topic = "/opendxl-domaintools/service/domaintools/domain_search"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domain tools"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "domain search" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Domain Search Documentation <https://www.domaintools.com/resources/api-documentation/domain-search/>`_:

    `"The Domain Search API searches for domain names that match your specific search string. Unlike Domain Suggestions, Domain Search finds
    currently registered or previously registered domain names that are either currently registered or have been registered in the past
    under one of the major gTLD's (.com, .net, .org, .info, .us, or .biz), many country code TLDs, or the new gTLDs."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.
