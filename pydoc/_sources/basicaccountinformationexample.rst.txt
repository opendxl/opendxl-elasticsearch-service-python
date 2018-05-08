Basic Account Information Example
=================================

This sample invokes and displays the results of a DomainTools "Account Information" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/account-information/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_account_information_example.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_account_information_example.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "response": {
                "account": {
                    "active": true,
                    "api_username": "username"
                },
                "products": [
                    {
                        "absolute_limit": null,
                        "expiration_date": null,
                        "id": "account-information",
                        "per_minute_limit": "5",
                        "per_month_limit": "100000",
                        "usage": {
                            "month": "0",
                            "today": "0"
                        }
                    },
                    {
                        "absolute_limit": "10000",
                        "expiration_date": "2017-07-18",
                        "id": "domain-profile",
                        "per_minute_limit": "120",
                        "per_month_limit": null,
                        "usage": {
                            "month": "0",
                            "today": "0"
                        }
                    },
                    {
                        "absolute_limit": "10000",
                        "expiration_date": "2017-07-18",
                        "id": "whois",
                        "per_minute_limit": "120",
                        "per_month_limit": null,
                        "usage": {
                            "month": "0",
                            "today": "0"
                        }
                    },
                    {
                        "absolute_limit": "1000",
                        "expiration_date": "2017-07-18",
                        "id": "whois-history",
                        "per_minute_limit": "30",
                        "per_month_limit": null,
                        "usage": {
                            "month": "0",
                            "today": "0"
                        }
                    },
                    {
                        "absolute_limit": "1000",
                        "expiration_date": "2017-07-18",
                        "id": "reverse-ip",
                        "per_minute_limit": "10",
                        "per_month_limit": null,
                        "usage": {
                            "month": "0",
                            "today": "0"
                        }
                    },
                    {
                        "absolute_limit": "1000",
                        "expiration_date": "2017-07-18",
                        "id": "reverse-name-server",
                        "per_minute_limit": "10",
                        "per_month_limit": null,
                        "usage": {
                            "month": "0",
                            "today": "0"
                        }
                    },
                    {
                        "absolute_limit": "10000",
                        "expiration_date": "2017-07-18",
                        "id": "parsed-whois",
                        "per_minute_limit": "120",
                        "per_month_limit": null,
                        "usage": {
                            "month": "0",
                            "today": "0"
                        }
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

            request_topic = "/opendxl-domaintools/service/domaintools/account_information"
            req = Request(request_topic)
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "account information" method
of the DomainTools API DXL service.

This does not require any payload and returns account information based on the API User value.

From the DomainTools `Account Information Documentation <https://www.domaintools.com/resources/api-documentation/account-information/>`_:

    `"The Account Information API provides a quick and easy way to get a snapshot of API product usage for an account.
    Usage is broken down by day and by month."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.
