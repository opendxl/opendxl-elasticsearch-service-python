Basic Iris Example
========================

This sample invokes and displays the results of a DomainTools "Iris" via DXL.

For more information see:
    https://www.domaintools.com/resources/api-documentation/iris/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DomainTools API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_iris_example.py`` script as follows:

     .. parsed-literal::

        python sample/basic/basic_iris_example.py


The output should appear similar to the following:

    .. code-block:: python

        {
          "response": {
            "limit_exceeded": false,
            "message": "Enjoy your data.",
            "results_count": 1,
            "results": [
              {
                "domain": "domaintools.com",
                "whois_url": "https://whois.domaintools.helium/domaintools.com",
                "adsense": "",
                "alexa": 2346,
                "google_analytics": 76641,
                "admin_contact": {
                  "name": "DOMAIN ADMINISTRATOR",
                  "org": "DOMAINTOOLS, LLC",
                  "street": "2101 4TH AVE,SUITE 1150",
                  "city": "SEATTLE",
                  "state": "WA",
                  "postal": "98121",
                  "country": "us",
                  "phone": "12068389035",
                  "fax": "12068389056",
                  "email": [
                    "memberservices@domaintools.com"
                  ]
                },
                "billing_contact": {
                  "name": "",
                  "org": "",
                  "street": "",
                  "city": "",
                  "state": "",
                  "postal": "",
                  "country": "",
                  "phone": "",
                  "fax": "",
                  "email": []
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

            request_topic = "/opendxl-domaintools/service/domaintools/iris"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"domain": "domaintools.com"})
            res = client.sync_request(req, timeout=30)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{}': {} ({})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "iris" method
of the DomainTools API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `domain` parameter
to report on.

From the DomainTools `Iris Pivot API Documentation <https://www.domaintools.com/resources/api-documentation/iris/>`_:

    `"The Iris Pivot API enables bulk enrichment of a list of domains with parsed domain and infrastructure profiles
    sourced from the Iris database. It also provides a multivariate search across several of the most commonly-used
    Iris data fields. Queries to the Iris Pivot API deduct from the same Iris query allocation assigned to a user's
    Enterprise Membership for qualified Iris customers."`

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.

