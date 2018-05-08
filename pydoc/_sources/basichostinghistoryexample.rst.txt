Basic Hosting History Example
=============================

This sample invokes and displays the results of a DomainTools "Hosting History" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/hosting-history/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_hosting_history_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_hosting_history_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "domain_name": "domaintools.com",
                "ip_history": [
                    {
                        "action": "N",
                        "action_in_words": "New",
                        "actiondate": "2004-05-03",
                        "domain": "DOMAINTOOLS.COM",
                        "post_ip": "63.247.77.156",
                        "pre_ip": null
                    },
                    {
                        "action": "C",
                        "action_in_words": "Change",
                        "actiondate": "2009-10-24",
                        "domain": "DOMAINTOOLS.COM",
                        "post_ip": "204.2.145.27",
                        "pre_ip": "209.107.205.90"
                    },
                    {
                        "action": "C",
                        "action_in_words": "Change",
                        "actiondate": "2009-11-03",
                        "domain": "DOMAINTOOLS.COM",
                        "post_ip": "209.107.205.90",
                        "pre_ip": "204.2.145.27"
                    },
                    .........
                    {
                        "action": "C",
                        "action_in_words": "Change",
                        "actiondate": "2015-04-02",
                        "domain": "DOMAINTOOLS.COM",
                        "post_ip": "199.30.228.112",
                        "pre_ip": "8.247.70.160"
                    }
                ],
                "nameserver_history": [
                    {
                        "action": "T",
                        "action_in_words": "Transfer",
                        "actiondate": "2002-04-14",
                        "domain": "DOMAINTOOLS.COM",
                        "post_mns": "Xxxnameservers.com",
                        "pre_mns": "Interland.net"
                    },
                    {
                        "action": "T",
                        "action_in_words": "Transfer",
                        "actiondate": "2004-11-25",
                        "domain": "DOMAINTOOLS.COM",
                        "post_mns": "Host.org",
                        "pre_mns": "Xxxnameservers.com"
                    },
                ],
                "registrar_history": [
                    {
                        "date_created": "1998-08-02",
                        "date_expires": "2003-08-01",
                        "date_lastchecked": "2003-06-28",
                        "date_updated": "2002-04-12",
                        "domain": "DOMAINTOOLS.COM",
                        "registrar": "Tucows",
                        "registrartag": "Tucows"
                    },
                    {
                        "date_created": "1998-08-02",
                        "date_expires": "2017-08-01",
                        "date_lastchecked": "2014-08-15",
                        "date_updated": "2014-07-24",
                        "domain": "DOMAINTOOLS.COM",
                        "registrar": "eNom.com",
                        "registrartag": "ENOM, INC."
                    }
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

            request_topic = "/opendxl-domaintools/service/domaintools/hosting_history"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"query": "domaintools.com"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "hosting history" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `query` parameter
to report on.

From the DomainTools `Hosting History Documentation <https://www.domaintools.com/resources/api-documentation/hosting-history/>`_:

    `"The Hosting History API provides a list of changes that have occurred in a Domain Name's registrar, IP address, and
    name servers. IP and name server events include	the value before and after the change and indicate the type of action
    that triggered the event."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.
