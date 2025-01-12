import json
import pandas as pd

def load_data(filename: str) -> list:
    """
    Load JSON data from a file.
    
    Args:
        filename (str): Path to the JSON file.
    
    Returns:
        list: List of product data.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def preprocess_data(products: list) -> pd.DataFrame:
    """
    Preprocess the product data to extract relevant fields.
    
    Args:
        products (list): List of product dictionaries.
    
    Returns:
        pd.DataFrame: Cleaned and structured product data.
    """
    processed_data = []

    for product in products:
        try:
            processed_data.append({
                "product_name": product.get("product_name", "Unknown"),
                "ingredients": product.get("ingredients_text", "N/A"),
                "energy_kcal": product.get("nutriments", {}).get("energy-kcal_100g", None),
                "protein_100g": product.get("nutriments", {}).get("proteins_100g", None),
                "fat_100g": product.get("nutriments", {}).get("fat_100g", None),
                "carbohydrates_100g": product.get("nutriments", {}).get("carbohydrates_100g", None),
                "allergens": product.get("allergens", "None"),
                "price": product.get("price", None),
                "rating": product.get("rating", None)
            })
        except KeyError as e:
            print(f"Skipping product due to missing key: {e}")
    
    return pd.DataFrame(processed_data)

def save_to_csv(data: pd.DataFrame, filename: str) -> None:
    """
    Save processed data to a CSV file.
    
    Args:
        data (pd.DataFrame): DataFrame containing processed data.
        filename (str): File name to save the CSV as.
    """
    data.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    raw_files = [
        "healthy_breakfast_data.json",
        "protein_bars_data.json",
        "protein_cookies_data.json",
        "protein_snacks_data.json",
        "protein_shakes_data.json"
    ]
    processed_files = [
        "healthy_breakfast_cleaned.csv",
        "protein_bars_cleaned.csv",
        "protein_cookies_cleaned.csv",
        "protein_snacks_cleaned.csv",
        "protein_shakes_cleaned.csv"
    ]

    for raw_file, processed_file in zip(raw_files, processed_files):
        print(f"Processing file: {raw_file}")
        raw_data = load_data(raw_file)
        cleaned_data = preprocess_data(raw_data)
        print(f"Extracted {len(cleaned_data)} valid entries from {raw_file}")
        save_to_csv(cleaned_data, processed_file)
