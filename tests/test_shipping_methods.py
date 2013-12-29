import random
import nose.tools
import zinc_suite

class TestShippingMethods(zinc_suite.ZincSuite):
    zinc_url_stub = "shipping_methods"

    num_products_range = [1,5]

    macys_product_ids = [
        "797196",
        "604407",
        "952548",
        "717903",
        "276906",
        "1046946",
        "695171"
        ]

    product_ids = {
        "macys": macys_product_ids
        }

    def test_shipping_methods(self):
        for i in xrange(self.num_tests):
            retailer = random.sample(self.product_ids.keys(), 1)[0]
            self.run_single(retailer)

    def run_single(self, retailer):
        products = self.generate_products(retailer)
        shipping_address = self.generate_shipping_address(retailer)
        payload = {
            "retailer": retailer,
            "products": products,
            "shipping_address": shipping_address
            }
        result = self.post_request(payload)
        self.verify_response(retailer, result)

    def verify_response(self, retailer, result):
        # TODO: write this verification
        pass

    def generate_products(self, retailer):
        product_ids = self.product_ids[retailer]
        num_products = random.randint(self.num_products_range[0],
                min(self.num_products_range[1], len(product_ids)))
        product_ids = random.sample(product_ids, num_products)

        result = []
        for product_id in product_ids:
            result.append({
                "product_id": random.sample(product_id, 1)[0],
                "quantity": 1
                })
        return result

    def generate_shipping_address(self, retailer):
        # TODO: actually generate shipping addresses
        return {
            "first_name": "Tim",
            "last_name": "Beaver",
            "address_line1": "77 Massachusetts Avenue",
            "address_line2": "",
            "zip_code": "02139",
            "city": "Cambridge", 
            "state": "MA",
            "country": "US",
            "phone_number": "5559583928"
            }
