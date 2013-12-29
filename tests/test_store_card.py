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
            card = random.sample(card_data, 1)[0]
            self.run_single(card)

    def run_single(self, card):
        # TODO: send the request
        result = self.post_request(payload)
        self.verify_response(retailer, result)

    def verify_response(self, retailer, result):
        #TODO: verify the response
