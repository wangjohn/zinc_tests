import random
import nose.tools
import zinc_suite
import collections

class TestShippingMethods(zinc_suite.ZincSuite):
    zinc_url_stub = "shipping_methods"
    num_products_range = [1,5]
    product_quantity_range = [1,4]
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
        data = self.process_data()
        for i in xrange(self.num_tests):
            self.run_single(data)

    def run_single(self, data):
        product_ids, _ = data
        retailer = random.sample(product_ids.keys(), 1)[0]
        products = self.generate_products(product_ids[retailer])
        return self.run_retailer_and_products(retailer, products, data)

    def run_retailer_and_products(self, retailer, products, data):
        _ , shipping_addresses = data
        shipping_address = self.generate_shipping_address(retailer, shipping_addresses)
        payload = {
            "retailer": retailer,
            "products": products,
            "shipping_address": shipping_address
            }
        result = self.post_request(payload)
        self.verify_response(retailer, result)
        return {"response": result, "shipping_address": shipping_address}

    def verify_response(self, retailer, result):
        nose.tools.assert_equals("shipping_methods_response", result["_type"])
        nose.tools.assert_equals(retailer, result["retailer"])
        nose.tools.assert_is_not_none(result["shipping_methods"])
        nose.tools.assert_greater_equal(len(result["shipping_methods"]), 0)

        for shipping_method in result["shipping_methods"]:
            nose.tools.assert_is_not_none(shipping_method["shipping_method_id"])
            nose.tools.assert_is_not_none(shipping_method["name"])
            nose.tools.assert_is_not_none(shipping_method["description"])
            nose.tools.assert_greater_equal(shipping_method["price"], 0)

    def generate_products(self, product_ids):
        num_products = random.randint(self.num_products_range[0],
                min(self.num_products_range[1], len(product_ids)))
        product_ids = random.sample(product_ids, num_products)

        result = []
        for product_id in product_ids:
            result.append({
                "product_id": product_id,
                "quantity": self.generate_product_quantity()
                })
        return result

    def generate_product_quantity(self):
        return random.randint(self.product_quantity_range[0],
                self.product_quantity_range[1])

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
