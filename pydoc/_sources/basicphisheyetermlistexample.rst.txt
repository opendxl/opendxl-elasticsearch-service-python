Basic PhishEye Term List Example
================================

This sample invokes and displays the results of a DomainTools "PhishEye Term List" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/phisheye/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_phisheye_term_list_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_phisheye_term_list_example.py


The output should appear similar to the following:

    .. code-block:: python

         {
            "response": {
              "terms": [
                {
                  "term": "apple",
                  "active": true,
                  "user_monitor_count": 2
                },
                {
                  "term": "chevrolet",
                  "active": true,
                  "user_monitor_count": 1
                },
                ...
                {
                  "term": "yahoo",
                  "active": false,
                  "user_monitor_count": 1
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

            request_topic = "/opendxl-domaintools/service/domaintools/phisheye_term_list"
            req = Request(request_topic)
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "phisheye term list" method
of the DomainTools API DXL service.

This does not require any payload and returns list of terms that are set up for this account.

From the DomainTools `PhishEye Term List Documentation <https://www.domaintools.com/resources/api-documentation/phisheye/>`_:

    `"This provides a list of terms that are set up for this account.
    The PhishEye API is only available via our Enterprise Solutions team, and is not included in a membership."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

