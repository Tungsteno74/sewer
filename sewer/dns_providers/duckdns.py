import urllib.parse
import requests

from . import common


class DuckDNSDns(common.BaseDns):

    dns_provider_name = "duckdns"

    def __init__(self, duckdns_token, DUCKDNS_API_BASE_URL="https://www.duckdns.org"):

        self.duckdns_token = duckdns_token
        self.HTTP_TIMEOUT = 65  # seconds

        if DUCKDNS_API_BASE_URL[-1] != "/":
            self.DUCKDNS_API_BASE_URL = DUCKDNS_API_BASE_URL + "/"
        else:
            self.DUCKDNS_API_BASE_URL = DUCKDNS_API_BASE_URL
        super(DuckDNSDns, self).__init__()

    def _common_dns_record(self, logger_info, domain_name, payload_end_arg):
        self.logger.info("{0}".format(logger_info))
        # if we have been given a wildcard name, strip wildcard
        domain_name = domain_name.lstrip("*.")

        url = urllib.parse.urljoin(self.DUCKDNS_API_BASE_URL, "update")

        payload = dict([("domains", domain_name), ("token", self.duckdns_token), payload_end_arg])
        update_duckdns_dns_record_response = requests.get(
            url, params=payload, timeout=self.HTTP_TIMEOUT
        )

        normalized_response = update_duckdns_dns_record_response.text
        self.logger.debug(
            "update_duckdns_dns_record_response. status_code={0}. response={1}".format(
                update_duckdns_dns_record_response.status_code, normalized_response
            )
        )

        if update_duckdns_dns_record_response.status_code != 200 or normalized_response != "OK":
            # raise error so that we do not continue to make calls to DuckDNS
            # server
            raise ValueError(
                "Error creating DuckDNS dns record: status_code={status_code} response={response}".format(
                    status_code=update_duckdns_dns_record_response.status_code,
                    response=normalized_response,
                )
            )
        self.logger.info("{0}_success".format(logger_info))

    def create_dns_record(self, domain_name, domain_dns_value):
        self._common_dns_record("create_dns_record", domain_name, ("txt", domain_dns_value))

    def delete_dns_record(self, domain_name, domain_dns_value):
        self._common_dns_record("delete_dns_record", domain_name, ("clear", "true"))
