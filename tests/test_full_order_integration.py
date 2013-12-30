import test_store_card
import test_variant_options
import test_shipping_methods

class TestFullOrderIntegration:

    def process_data(self):
        data = {}
        data["store_card"] = test_store_card.TestStoreCard.process_data()
        data["variant_options"] = test_variant_options.TestVariantOptions.process_data()
        data["shipping_methods"] = test_shipping_methods.TestShippingMethods.process_data()
        return data

    def test_full_order_integration(self):
        test_store_card.TestStoreCard.run_single(
        pass
