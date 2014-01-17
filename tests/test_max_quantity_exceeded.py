import random
import nose.tools
import zinc_suite
import collections

class TestMaxQuantityExceeded(zinc_suite.ZincSuite):

    def generate_data_filenames(retailers):
        data_filenames = ["shipping_addresses.csv"]
        for retailer in retailers:
            data_filenames.append(retailer + "/max_quantity_exceeded.csv")
        return data_filenames

    zinc_url_stub = "shipping_methods"
    num_products_range = [1,5]
    data_filenames = generate_data_filenames(zinc_suite.ZincSuite.retailers)

    def process_data(self):
        shipping_methods = collections.defaultdict(list)
        shipping_addresses = []

        for retailer, line, filename in self.read_data():
            if filename.endswith("product_unavailable.csv"):
                shipping_methods[retailer].append(line)
            else:
                shipping_addresses.append(line)

        return (shipping_methods, shipping_addresses)

    def test_shipping_methods(self):
        data = self.process_data()
        for i in xrange(self.num_tests):
            self.run_single(data)

    def run_single(self, data):
        products_hash, _ = data
        retailer = random.sample(products_hash.keys(), 1)[0]
        products = self.generate_products(products_hash[retailer])
        return self.run_retailer_and_products(retailer, products, data)

    def run_retailer_and_products(self, retailer, products, data):
        _ , shipping_addresses = data
        shipping_address = self.generate_shipping_address(retailer, shipping_addresses)
        payload = {
            "client_token": "zinc_monkey",
            "retailer": retailer,
            "products": products,
            "shipping_address": shipping_address
            }
        result = self.post_request(payload)
        self.verify_response(retailer, result)
        return {"response": result, "shipping_address": shipping_address}

    def verify_response(self, retailer, result):
        nose.tools.assert_equals("error", result["_type"])
        nose.tools.assert_equals("max_quantity_exceeded", result["code"])

    def generate_products(self, products_list):
        num_products = random.randint(self.num_products_range[0],
                min(self.num_products_range[1], len(product_ids)))
        products_used = random.sample(product_ids, num_products)

        result = []
        for product in products_used:
            result.append({
                "product_id": product[0],
                "quantity": product[1]
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
