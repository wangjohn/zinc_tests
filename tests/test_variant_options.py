import random
import nose.tools
import zinc_suite
import collections

class TestVariantOptions(zinc_suite.ZincSuite):
    zinc_url_stub = "variant_options"

    def process_data(self):
        data = collections.defaultdict(list)
        for line, filename in self.read_data():
            data[line[0]].append(line[1])
        return data

    def test_variant_options(self):
        product_urls = self.process_data()
        for i in xrange(self.num_tests):
            self.run_single(product_urls)

    def run_single(self, product_urls):
        retailer = random.sample(product_urls.keys(), 1)[0]
        url = self.generate_product_url(retailer, product_urls)
        payload = {
            "retailer": retailer,
            "product_url": url
            }
        result = self.post_request(payload)
        self.verify_response(retailer, url, result)
        return result

    def verify_response(self, retailer, url, result):
        nose.tools.assert_equals("variant_options_response", result["_type"])
        nose.tools.assert_equals(retailer, result["retailer"])
        nose.tools.assert_equals(url, result["product_url"])
        nose.tools.assert_is_not_none(result["variant_options"])
        nose.tools.assert_greater_equal(len(result["variant_options"]), 0)

        for variant_option in result["variant_options"]:
            nose.tools.assert_equals("variant_option", variant_option["_type"])
            nose.tools.assert_greater_equal(variant_option["unit_price"], 0)
            nose.tools.assert_is_not_none(variant_option["product_id"])
            nose.tools.assert_is_not_none(variant_option["dimensions"])
            for dimension in variant_option["dimensions"]:
                nose.tools.assert_is_not_none(dimension["name"])
                nose.tools.assert_is_not_none(dimension["value"])

    def generate_product_url(self, retailer, product_urls):
        retailer_urls = product_urls[retailer]
        return random.sample(retailer_urls, 1)[0]
