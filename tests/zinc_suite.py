import requests
import json

class ZincSuite:
    num_tests = 1

    def post_request(self, url, payload):
        result = requests.post(url, data=json.dumps(payload))
        request_id = result.json()["request_id"]
        return self.wait_for_response(url, request_id)

    def wait_for_response(self, url, request_id):
        result = requests.get(url + "/" + request_id)
        result_json = result.json()
        if result_json["_type"] == "error" and result_json["code"] == "request_processing":
            return self.wait_for_response(url, request_id)
        else:
            return result_json
