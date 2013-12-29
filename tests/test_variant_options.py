import random
import nose.tools
import zinc_suite

class TestVariantOptions(zinc_suite.ZincSuite):
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
            for dimension in variant_option["dimensions"]:
                nose.tools.assert_is_not_none(dimension["name"])
                nose.tools.assert_is_not_none(dimension["value"])

    def generate_product_url(self, retailer):
        retailer_urls = self.product_urls[retailer]
        return random.sample(retailer_urls, 1)[0]
