Basic IP Registrant Monitor Example
===================================

This sample invokes and displays the results of a DomainTools "IP Registrant Monitor" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/ip-registrant-monitor/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_ip_registrant_monitor_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_ip_registrant_monitor_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "record_count": 99,
                "modified": [],
                "page": 1,
                "added": [
                    {
                        "ip_to": "51.255.100.255",
                        "organization": "INTERNAL USAGE",
                        "record_ip": "51.255.100.255",
                        "record_date": "2016-01-05",
                        "range": "51.255.100.224/27",
                        "ip_from": "51.255.100.224",
                        "server": "whois.ripe.net",
                        "country": "FR"
                    },
                    {
                        "ip_to": "51.254.170.239",
                        "organization": "PrivateCloud id -831",
                        "record_ip": "51.254.170.224",
                        "record_date": "2016-01-05",
                        "range": "51.254.170.224/28",
                        "ip_from": "51.254.170.224",
                        "server": "whois.ripe.net",
                        "country": "FR"
                    },
                    ...
                ],
                "removed": [
                    {
                        "ip_to": "46.105.155.183",
                        "record_ip": "46.105.155.177",
                        "record_date": "2015-03-09",
                        "range": "46.105.155.176/29",
                        "ip_from": "46.105.155.176",
                        "organization": "usertestro",
                        "server": "whois.ripe.net",
                        "country": "FR"
                    },
                    {
                        "ip_to": "37.59.91.175",
                        "record_ip": "37.59.91.163",
                        "record_date": "2015-02-13",
                        "range": "37.59.91.160/28",
                        "ip_from": "37.59.91.160",
                        "organization": "SP&PS",
                        "server": "whois.ripe.net",
                        "country": "FR"
                    },
                    ...
                ],
                "has_more_pages": false,
                "date": "2016-01-06",
                "query": "ovh"
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

            request_topic = "/opendxl-domaintools/service/domaintools/ip_registrant_monitor"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "ip registrant monitor" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `IP Registrant Monitor API Documentation <https://www.domaintools.com/resources/api-documentation/ip-registrant-monitor/>`_:

    `"The IP Registrant Monitor API searches the ownership (Whois) records of domain names for specific search terms.
    The product is ideal for monitoring specific domain owners (such as "DomainTools LLC") to be alerted whenever their information
    appears in a newly-registered domain name. The API will also alert you to domains that no longer match a specific term."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

