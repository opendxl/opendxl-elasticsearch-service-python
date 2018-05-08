Basic Host Domains Example
==========================

This sample invokes and displays the results of a DomainTools "Host Domains" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/reverse-ip/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_host_domains_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_host_domains_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "ip_addresses": {
                    "domain_count": 1,
                    "domain_names": [
                        "DAILYCHANGES.COM"
                    ],
                    "ip_address": "64.246.165.240"
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

            request_topic = "/opendxl-domaintools/service/domaintools/host_domains"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"ip": "64.246.165.240"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "host domains" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `ip` parameter
to report on.

From the DomainTools `Host Domains Documentation <https://www.domaintools.com/resources/api-documentation/reverse-ip/>`_:

    `"The Reverse IP API provides a list of domain names that share the same Internet host (i.e. the same IP address).
    You can request an IP address directly, or you can provide a domain name; if you provide a domain name, the API
    will respond with the list of other domains that share the same IP."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.
