import requests
import json
import os
import csv

class ZincSuite:
    num_tests = 1
    zinc_base_url = "https://demotwo.zinc.io/v0"
    zinc_url_stub = None
    data_filenames = None
    test_data_path = os.path.join(os.path.dirname(__file__), "../test_data/")

    def read_data(self):
        if self.data_filenames == None:
            filenames = [os.path.join(self.test_data_path,
                self.zinc_url_stub + ".csv")]
        else:
            filenames = []
            for filename_stub in self.data_filenames:
                filenames.append(os.path.join(self.test_data_path, filename_stub))

        for filename in filenames:
            with open(filename, "rb") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for line in reader:
                    yield line, filename

    def current_url(self):
        if self.zinc_url_stub:
            return self.zinc_base_url + "/" + self.zinc_url_stub
        else:
            return self.zinc_base_url

    def post_request(self, payload):
        result = requests.post(self.current_url(), data=json.dumps(payload))
        request_id = result.json()["request_id"]
        return self.wait_for_response(self.current_url(), request_id)

    def wait_for_response(self, url, request_id):
        result = requests.get(url + "/" + request_id)
        result_json = result.json()
        if result_json["_type"] == "error" and result_json["code"] == "request_processing":
            return self.wait_for_response(url, request_id)
        else:
            return result_json
