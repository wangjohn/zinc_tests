from test_store_card import TestStoreCard
from test_variant_options import TestVariantOptions
from test_shipping_methods import TestShippingMethods

class TestFullOrderIntegration:

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
        data["store_card"] = klasses["store_card"].process_data()
        data["variant_options"] = klasses["variant_options"].process_data()
        data["shipping_methods"] = klasses["shipping_methods"].process_data()
        return data

    def test_full_order_integration(self):
        klasses = self.create_klasses()
        data = self.process_data(klasses)

        for i in xrange(self.num_tests):
            klasses["store_card"].run_single(data["store_card"])
            klasses["variant_options"].run_single(data["variant_options"])
            klasses["shipping_methods"].run_single(data["shipping_methods"])


