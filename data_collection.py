import requests
import json

BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"

def fetch_category_data(category: str, page_size: int = 100, page: int = 1) -> list:
    """
    Fetch product data from OpenFoodFacts for a specific category.
    
    Args:
        category (str): The category to search for.
        page_size (int): Number of products to fetch per page.
        page (int): Page number for pagination.
    
    Returns:
        list: List of product data.
    """
    params = {
        'search_terms': category,
        'page_size': page_size,
        'page': page,
        'json': 1  # Request JSON format
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('products', [])
    else:
        print(f"Failed to fetch data for category '{category}'. Status code: {response.status_code}")
        return []

def save_data_to_file(data: list, filename: str) -> None:
    """
    Save JSON data to a file.
    
    Args:
        data (list): List of product data to save.
        filename (str): File name to save the data as.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    categories = {
        "healthy_breakfast": "breakfast-cereals",
        "protein_bars": "protein-bars",
        "protein_cookies": "protein-cookies",
        "protein_snacks": "protein-snacks",
        "protein_shakes": "protein-shakes"
    }

    for category_name, category_search in categories.items():
        print(f"Fetching data for category: {category_name} ({category_search})")
        products = fetch_category_data(category_search, page_size=100, page=1)
        print(f"Fetched {len(products)} products for category '{category_name}'.")
        
        if products:
            filename = f"{category_name}_data.json"
            save_data_to_file(products, filename)
            print(f"Data saved to {filename}")
        else:
            print(f"No products found for category '{category_name}'.")
