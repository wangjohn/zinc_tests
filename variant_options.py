import requests


class TestVariantOptions:

    zinc_url = "https://demotwo.zinc.io/v0/variant_options"

    macys_urls = [
        "http://www1.macys.com/shop/product/nike-dri-fit-shirt-swoosh-tennis-polo?ID=797196",
        "http://www1.macys.com/shop/product/puma-shirt-ferrari-shield-polo?ID=604407",
        "http://www1.macys.com/shop/product/greg-norman-for-tasso-elba-golf-shirt-short-sleeve-heathered-striped-performance-polo?ID=952548",
        "http://www1.macys.com/shop/product/perry-ellis-portfoilio-travel-kit?ID=717903",
        "http://www1.macys.com/shop/product/kenneth-cole-reaction-colombian-leather-single-gusset-messenger-bag?ID=276906",
        "http://www1.macys.com/shop/product/7-for-all-mankind-jeans-kimmie-straight-leg-la-verna-lake-wash?ID=1046946",
        "http://www1.macys.com/shop/product/levis-529-curvy-bootcut-jeans-right-on-blue-wash?ID=695171"
        ]

    def run_test(retailer, url):
        requests.post(zinc_url, 
