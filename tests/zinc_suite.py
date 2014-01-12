import requests
import json
import os
import csv
import logging
import time

def create_logger(filename):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    full_path = os.path.join(directory, filename)
    logging.basicConfig(filename=full_path, level=logging.INFO,
            format='%(asctime)s|%(name)s|%(levelname)s|%(message)s',
            datefmt='%m/%d/%Y %I:%M:%S%p')
    logger = logging.getLogger(__name__)
    return logger

class ZincSuite:
    num_tests = 1
    # zinc_base_url = "https://demotwo.zinc.io/v0"
    zinc_base_url = "http://localhost:5000/v0"
    zinc_url_stub = None
    data_filenames = None
    test_data_path = os.path.join(os.path.dirname(__file__), "../test_data/")
    logger = create_logger("tests.log")
    retailers = ['amazon']

    def read_data(self):
        for retailer in self.retailers:
            if self.data_filenames == None:
                retailer_path = os.path.join(self.test_data_path, retailer, self.zinc_url_stub + ".csv")
                non_retailer_path = os.path.join(self.test_data_path, self.zinc_url_stub + ".csv")
                print os.path.exists(retailer_path)
                print os.path.exists(non_retailer_path)
                if os.path.exists(retailer_path):
                    filenames = [retailer_path]
                elif os.path.exists(non_retailer_path):
                    filenames = [non_retailer_path]
                else:
                    filenames = []

            else:
                filenames = []
                for filename_stub in self.data_filenames:
                    filenames.append(os.path.join(self.test_data_path, filename_stub))

            for filename in filenames:
                with open(filename, "rb") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for line in reader:
                        yield retailer, line, filename

    def current_url(self):
        if self.zinc_url_stub:
            return self.zinc_base_url + "/" + self.zinc_url_stub
        else:
            return self.zinc_base_url

    def post_request(self, payload, client_token = "zinc_monkey"):
        if "client_token" not in payload:
            payload["client_token"] = client_token
        self.logger.warn("Posting request. Url: %s, data: %s", self.current_url(), payload)
        start_time = time.time()
        result = requests.post(self.current_url(), data=json.dumps(payload))
        request_id = result.json()["request_id"]
        self.logger.warn("Request posted. Request id: %s", request_id)
        return self.wait_for_response(self.current_url(), request_id, start_time)

    def wait_for_response(self, url, request_id, start_time):
        result = requests.get(url + "/" + request_id)
        result_json = result.json()
        if result_json["_type"] == "error" and result_json["code"] == "request_processing":
            return self.wait_for_response(url, request_id, start_time)
        else:
            end_time = time.time()
            self.logger.warn("Request '%s' time: %s", request_id, end_time - start_time)
            self.logger.warn("Received response: %s", result_json)
            return result_json
