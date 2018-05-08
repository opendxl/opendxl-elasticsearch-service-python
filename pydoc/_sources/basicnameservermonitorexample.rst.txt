Basic Name Server Monitor Example
=================================

This sample invokes and displays the results of a DomainTools "Name Server Monitor" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/name-server-monitor/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_name_server_monitor_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_name_server_monitor_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "alerts": [
                    {
                        "action": "Transfer Out",
                        "domain": "00000000000.PW",
                        "new_name_server": "i-now.cn",
                        "old_name_server": "dnspod.net"
                    },
                    {
                        "action": "New",
                        "domain": "1524PPP.COM",
                        "new_name_server": "dnspod.net",
                        "old_name_server": ""
                    },
                    {
                        "action": "New",
                        "domain": "1524QQ.COM",
                        "new_name_server": "dnspod.net",
                        "old_name_server": ""
                    },
                    ...
                ],
                "date": "2017-07-18",
                "limit": 1000,
                "name_server": "DNSPOD.NET",
                "page": 1,
                "page_count": 35,
                "total": "34494"
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

            request_topic = "/opendxl-domaintools/service/domaintools/name_server_monitor"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "DNSPOD.NET"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "name server monitor" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Name Server Monitor Documentation <https://www.domaintools.com/resources/api-documentation/name-server-monitor/>`_:

    `"The Name Server Monitor API searches the daily activity of all our monitored TLDs on any given name server. New, Deleted
    and Transferred domains records can be queried up to 6 days in the past."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

