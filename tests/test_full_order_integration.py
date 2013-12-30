from test_store_card import TestStoreCard
from test_variant_options import TestVariantOptions
from test_shipping_methods import TestShippingMethods
import random
import zinc_suite

class TestFullOrderIntegration(zinc_suite.ZincSuite):
    zinc_url_stub = "review_order"

    def create_klasses(self):
        klasses = {}
        klasses["store_card"] = TestStoreCard()
        klasses["variant_options"] = TestVariantOptions()
        klasses["shipping_methods"] = TestShippingMethods()

        for klass in klasses.itervalues():
            klass.num_tests = 1
        return klasses

    def process_data(self, klasses):
        data = {}
        for klass_type, klass in klasses.iteritems():
            data[klass_type] = klass.process_data()
        return data

    def test_full_order_integration(self):
        klasses = self.create_klasses()
        data = self.process_data(klasses)

        for i in xrange(self.num_tests):
            self.run_review_order(klasses, data)

    def run_review_order(self, klasses, data):
        results = {}
        results["variant_options"] = klasses["variant_options"].run_single(data["variant_options"])
        selected_retailer = self.select_retailer(results["variant_options"], klasses)
        selected_variants = self.select_product_variants(results["variant_options"], klasses)

        results["shipping_methods"] = klasses["shipping_methods"].run_retailer_and_products(selected_retailer, selected_variants, data["shipping_methods"])
        selected_shipping_id = self.select_shipping_id(results["shipping_methods"], klasses)
        selected_shipping_address = self.select_shipping_address(results["shipping_methods"], klasses)

        results["store_card"] = klasses["store_card"].run_single(data["store_card"])
        selected_payment_method = self.select_payment_method(results["store_card"], klasses)

        review_order_payload = {
                "retailer": selected_retailer,
                "products": selected_variants,
                "shipping_address": selected_shipping_address,
                "is_gift": false,
                "shipping_method_id": selected_shipping_id,
                "payment_method": selected_payment_method,
                "customer_email": email_address
                }
        result = self.post_request(review_order_payload)
        return result

    def verify_review_order_result(self, result, payload):
        nose.tools.assert_equals("review_order_response", result["_type"])
        nose.tools.assert_equals(payload["retailer"], result["retailer"])
        nose.tools.assert_is_not_none(result["place_order_key"])
        nose.tools.assert_is_not_none(result["price_components"])
        nose.tools.assert_greater_equal(result["price_components"]["total"])
        nose.tools.assert_greater_equal(result["price_components"]["tax"])
        nose.tools.assert_greater_equal(result["price_components"]["shipping"])
        nose.tools.assert_greater_equal(result["price_components"]["subtotal"])

    def select_retailer(self, variant_options_results, klasses):
        return variant_options_results["retailer"]

    def select_product_variants(self, variant_options_results, klasses):
        options = variant_options_results["variant_options"]
        product_ids = [option["product_id"] for option in options]
        return klasses["shipping_methods"].generate_products(options)

    def select_shipping_id(self, shipping_methods_results, klasses):
        methods = shipping_methods_results["response"]["shipping_methods"]
        selected = random.sample(methods, 1)[0]
        return selected["shipping_method_id"]

    def select_shipping_address(self, shipping_method_results, klasses):
        return selected_method_results["shipping_address"]

    def select_payment_method(self, store_card_results, klasses):
        return {
                "security_code": store_card_results["security_code"],
                "cc_token": store_card_results["response"]["cc_token"]
                }
