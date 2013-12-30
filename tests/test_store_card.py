import random
import nose.tools
import zinc_suite
import collections

class TestStoreCard(zinc_suite.ZincSuite):
    zinc_url_stub = "store_card"

    def process_data(self):
        card_data = []
        for line, filename in self.read_data():
            card_data.append(line)

        return card_data

    def test_store_card(self):
        card_data = self.process_data()
        for i in xrange(self.num_tests):
            self.run_single(card_data)

    def run_single(self, card_data):
        card = random.sample(card_data, 1)[0]
        payload = self.create_payload(card)
        result = self.post_request(payload)
        self.verify_response(result, payload)
        return {"response": result, "security_code": card[11]}

    def verify_response(self, result, request_payload):
        nose.tools.assert_equals("store_card_response", result["_type"])
        nose.tools.assert_is_not_none(result["cc_token"])
        nose.tools.assert_is_not_none(result["last_four"])
        nose.tools.assert_is_not_none(result["brand"])

        billing_result = result["billing_address"]
        billing_payload = request_payload["billing_address"]
        nose.tools.assert_equals(len(billing_result), len(billing_payload))
        for key, val in billing_result.iteritems():
            nose.tools.assert_equals(val, billing_payload[key])

    def create_payload(self, card):
        return {
                "number": card[0],
                "expiration_month": card[1],
                "expiration_year": card[2],
                "billing_address": {
                    "first_name": card[3],
                    "last_name": card[4],
                    "address_line1": card[5],
                    "address_line2": card[6],
                    "zip_code": card[7],
                    "city": card[8],
                    "state": card[9],
                    "country": card[10]
                    }
                }
