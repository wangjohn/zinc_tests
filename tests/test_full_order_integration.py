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
        for klass_type, klass in klasses.iteritems():
            data[klass_type] = klass.process_data()
        return data

    def test_full_order_integration(self):
        klasses = self.create_klasses()
        data = self.process_data(klasses)

        for i in xrange(self.num_tests):
            self.run_single(klasses, data)

    def run_review_order(self, klasses, data):
        result = {}
        for klass_type, klass in klasses.iteritems():
            result[klass_type] = klass.run_single(data[klass_type])

        #TODO: I think I actually have to run something from beginning to end.

