import random
import nose.tools
import zinc_suite
import collections

class TestShippingMethods(zinc_suite.ZincSuite):
    zinc_url_stub = "shipping_methods"
    num_products_range = [1,5]
    data_filenames = ["shipping_methods.csv", "shipping_addresses.csv"]

    def process_data(self):
        shipping_methods = collections.defaultdict(list)
        shipping_addresses = []

        for line, filename in self.read_data():
            if filename.endswith("shipping_methods.csv"):
                shipping_methods[line[0]].append(line[1])
            else:
                shipping_addresses.append(line)

        return (shipping_methods, shipping_addresses)

    def test_shipping_methods(self):
        (product_ids, shipping_addresses) = self.process_data()
        for i in xrange(self.num_tests):
            retailer = random.sample(product_ids.keys(), 1)[0]
            self.run_single(retailer, product_ids, shipping_addresses)

    def run_single(self, retailer, product_ids, shipping_addresses):
        products = self.generate_products(retailer, product_ids)
        shipping_address = self.generate_shipping_address(retailer, shipping_addresses)
        payload = {
            "retailer": retailer,
            "products": products,
            "shipping_address": shipping_address
            }
        result = self.post_request(payload)
        self.verify_response(retailer, result)

    def verify_response(self, retailer, result):
        print result
        nose.tools.assert_equals("shipping_methods_reponse", result["_type"])
        nose.tools.assert_equals(retailer, result["retailer"])
        nose.tools.assert_is_not_none(result["shipping_methods"])
        nose.tools.assert_greater_equal(len(result["shipping_methods"]), 0)

        for shipping_method in result["shipping_methods"]:
            nose.tools.assert_is_not_none(shipping_method["shipping_method_id"])
            nose.tools.assert_is_not_none(shipping_method["name"])
            nose.tools.assert_is_not_none(shipping_method["description"])
            nose.tools.assert_greater_equal(shipping_method["price"], 0)

    def generate_products(self, retailer, product_ids):
        pids = product_ids[retailer]
        num_products = random.randint(self.num_products_range[0],
                min(self.num_products_range[1], len(pids)))
        pids = random.sample(pids, num_products)

        result = []
        for product_id in pids:
            result.append({
                "product_id": product_id,
                "quantity": 1
                })
        return result

    def generate_shipping_address(self, retailer, shipping_addresses):
        address = random.sample(shipping_addresses, 1)[0]
        return {
                "first_name": address[0],
                "last_name": address[1],
                "address_line1": address[2],
                "address_line2": address[3],
                "zip_code": address[4],
                "city": address[5],
                "state": address[6],
                "country": address[7],
                "phone_number": address[8]
                }
