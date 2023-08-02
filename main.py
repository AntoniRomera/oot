from oot import Oot, Field, api
import logging
import requests
import time
import datetime

_logger = logging.getLogger(__name__)


class BioStarApi:

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.last_datetime = None

    def _generate_request_data(self):
        _logger.info("_generate_request_data")
        return {}

    def read_access_control(self):
        _logger.info("read_access_control")
        data = self._generate_request_data()
        response = requests.request("GET", self.host, data=data)
        self.last_datetime = datetime.datetime.now()

        return response.json()


class DemoOot(Oot):
    """  """
    biostar_host = Field(name="Biostar Host", required=True)
    biostar_port = Field(name="Biostar Port", required=True)
    biostar_user = Field(name="Biostar User", required=True)
    biostar_pass = Field(name="Biostar Password", required=True)

    def __init__(self, connection, file_path):
        super().__init__(connection, file_path)
        self.biostar_api = BioStarApi(self.biostar_host, self.biostar_port, self.biostar_user, self.biostar_pass)

    @api.oot
    def get_data_biostar(self, **kwargs):
        """"""
        time.sleep(5.0)
        while True:
            data = self.biostar_api.read_access_control()
            if data:
                _logger.info("Sending %s" % data)
                return data

    def process_result(self, key, result, **kwargs):
        _logger.info("For %s, we received the following result: %s" % (key, result))
        return super().process_result(key, result, **kwargs)


DemoOot({
    "host": "192.168.101.205:8069"
}).run()
