import requests

BASE_URL = "https://dummyjson.com/products"

def get_all_products(limit=30):
    return requests.get(f"{BASE_URL}?limit={limit}").json()

def get_product_by_id(product_id):
    return requests.get(f"{BASE_URL}/{product_id}").json()

def search_products(query):
    return requests.get(f"{BASE_URL}/search?q={query}").json()
import requests
def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns:
        list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises error for 4xx/5xx

        data = response.json()
        products = data.get("products", [])

        print("✅ Successfully fetched products from API")
        return products

    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch products:", e)
        return []
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product information

    Parameters:
        api_products: list returned from fetch_all_products()

    Returns:
        dict mapping product ID to product info
    """

    product_map = {}

    for product in api_products:
        product_id = product.get("id")

        product_map[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_map
