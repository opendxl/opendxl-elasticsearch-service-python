Basic Reverse IP Whois Example
==============================

This sample invokes and displays the results of a DomainTools "Reverse IP Whois" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/reverse-ip-whois/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_reverse_ip_whois_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_reverse_ip_whois_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
          "response": {
            "has_more_pages": true,
            "page": 1,
            "total_count": 1105,
            "record_count": 1000,
            "records": [
              {
                "ip_from": "1.179.248.0",
                "ip_to": "1.179.255.255",
                "record_ip": "1.179.249.17",
                "record_date": "2015-05-15",
                "server": "whois.apnic.net",
                "organization": "Static IP address for Google-caching servers",
                "country": "TH",
                "range": "1.179.248.0/21"
              },
              {
                "ip_from": "4.3.2.0",
                "ip_to": "4.3.2.255",
                "record_ip": "4.3.2.1",
                "record_date": "2015-05-17",
                "server": "whois.arin.net",
                "organization": "Google Inc.",
                "country": "US",
                "range": "4.3.2.0/24"
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

            request_topic = "/opendxl-domaintools/service/domaintools/reverse_ip_whois"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "google"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "reverse ip whois" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Reverse IP Whois Documentation <https://www.domaintools.com/resources/api-documentation/reverse-ip-whois/>`_:

    `"The Reverse IP Whois API provides a list of IP ranges that are owned by an Organization. You can enter an organization’s
    name and receive a list of all of the organization’s currently owned IP ranges."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

