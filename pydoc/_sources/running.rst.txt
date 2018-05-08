Running
=======

Once the DomainTools DXL service has been installed and the configuration files are populated it can be started by
executing the following command line:

    .. parsed-literal::

        python -m dxldomaintoolsservice <configuration-directory>

    The ``<configuration-directory>`` argument must point to a directory containing the configuration files
    required for the application (see :doc:`configuration`).

For example:

    .. parsed-literal::

        python -m dxldomaintoolsservice config

Output
------

The output from starting the service should appear similar to the following:

    .. parsed-literal::

        Running application ...
        On 'run' callback.
        On 'load configuration' callback.
        Incoming message configuration: queueSize=1000, threadCount=10
        Message callback configuration: queueSize=1000, threadCount=10
        Attempting to connect to DXL fabric ...
        Connected to DXL fabric.
        Registering service: domaintools_service
        Registering request callback: domaintools_account_information_requesthandler
        Registering request callback: domaintools_brand_monitor_requesthandler
        Registering request callback: domaintools_domain_profile_requesthandler
        Registering request callback: domaintools_domain_search_requesthandler
        Registering request callback: domaintools_domain_suggestions_requesthandler
        Registering request callback: domaintools_hosting_history_requesthandler
        Registering request callback: domaintools_ip_monitor_requesthandler
        Registering request callback: domaintools_ip_registrant_monitor_requesthandler
        Registering request callback: domaintools_name_server_monitor_requesthandler
        Registering request callback: domaintools_parsed_whois_requesthandler
        Registering request callback: domaintools_registrant_monitor_requesthandler
        Registering request callback: domaintools_reputation_requesthandler
        Registering request callback: domaintools_reverse_ip_requesthandler
        Registering request callback: domaintools_host_domains_requesthandler
        Registering request callback: domaintools_reverse_ip_whois_requesthandler
        Registering request callback: domaintools_reverse_name_server_requesthandler
        Registering request callback: domaintools_reverse_whois_requesthandler
        Registering request callback: domaintools_whois_requesthandler
        Registering request callback: domaintools_whois_history_requesthandler
        Registering request callback: domaintools_phisheye_requesthandler
        Registering request callback: domaintools_phisheye_term_list_requesthandler
        Registering request callback: domaintools_iris_requesthandler
        On 'DXL connect' callback.