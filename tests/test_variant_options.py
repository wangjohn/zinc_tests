import requests
import json
import random
import nose.tools

class ZincSuite:
    num_tests = 500

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

class TestVariantOptions(ZincSuite):
    zinc_url = "https://demotwo.zinc.io/v0/variant_options"

    macys_product_urls = [
        "http://www1.macys.com/shop/product/nike-dri-fit-shirt-swoosh-tennis-polo?ID=797196",
        "http://www1.macys.com/shop/product/puma-shirt-ferrari-shield-polo?ID=604407",
        "http://www1.macys.com/shop/product/greg-norman-for-tasso-elba-golf-shirt-short-sleeve-heathered-striped-performance-polo?ID=952548",
        "http://www1.macys.com/shop/product/perry-ellis-portfoilio-travel-kit?ID=717903",
        "http://www1.macys.com/shop/product/kenneth-cole-reaction-colombian-leather-single-gusset-messenger-bag?ID=276906",
        "http://www1.macys.com/shop/product/7-for-all-mankind-jeans-kimmie-straight-leg-la-verna-lake-wash?ID=1046946",
        "http://www1.macys.com/shop/product/levis-529-curvy-bootcut-jeans-right-on-blue-wash?ID=695171"
        ]

    product_urls = {
        "macys": macys_product_urls
        }

    def test_variant_options(self):
        for i in xrange(self.num_tests):
            retailer = random.sample(self.product_urls.keys(), 1)[0]
            self.run_single(retailer)

    def run_single(self, retailer):
        url = self.generate_product_url(retailer)
        payload = {
            "retailer": retailer,
            "product_url": url
            }
        result = self.post_request(self.zinc_url, payload)
        self.verify_response(retailer, url, result)

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

    def generate_product_url(self, retailer):
        retailer_urls = self.product_urls[retailer]
        return random.sample(retailer_urls, 1)[0]
