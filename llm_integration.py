import os
from dotenv import load_dotenv
import openai
import pandas as pd

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please ensure it's set in the .env file.")

def load_data(filenames: dict) -> dict:
    data = {}
    for category, file in filenames.items():
        data[category] = pd.read_csv(file)
    return data

def query_data(category_data: pd.DataFrame, query: str) -> pd.DataFrame:
    if "highest protein" in query and "price" in query:
        category_data["protein_per_price"] = category_data["protein_100g"] / category_data["price"]
        return category_data.sort_values("protein_per_price", ascending=False).head(3)
    elif "highest protein" in query:
        return category_data.sort_values("protein_100g", ascending=False).head(3)
    elif "low calorie" in query:
        return category_data.sort_values("energy_kcal", ascending=True).head(5)
    elif "under $2" in query:
        return category_data[category_data["price"] < 2]
    elif "5-star rating" in query:
        return category_data[category_data["rating"] == 5]
    elif "gluten-free" in query:
        return category_data[category_data["allergens"].str.contains("gluten", case=False) == False]
    else:
        return category_data

def generate_response(data: pd.DataFrame, query: str) -> str:
    """
    Use OpenAI to generate a natural language response based on query and data.
    """
    if data.empty:
        return "No matching data found for the query."

    # Summarize the dataset for GPT
    data_summary = data.to_dict(orient="records")
    total_products = len(data)

    # Construct a detailed prompt
    prompt = f"""
    You are an expert assistant for analyzing food product datasets. The user has asked the following question:
    "{query}"

    Here is a summary of the top {total_products} matching products:
    {data_summary}

    Please provide:
    1. A detailed answer to the query.
    2. Key insights from the dataset.
    3. Suggestions for the user based on their query.
    """

    try:
        # Chat completion request
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant analyzing food product datasets."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.AuthenticationError:
        return "Invalid API key. Please check your API key and try again."
    except openai.error.RateLimitError:
        return "Rate limit exceeded. Check your usage and billing details."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    files = {
        "Healthy Breakfast": "healthy_breakfast_cleaned.csv",
        "Protein Bars": "protein_bars_cleaned.csv",
        "Protein Cookies": "protein_cookies_cleaned.csv",
        "Protein Snacks": "protein_snacks_cleaned.csv",
        "Protein Shakes": "protein_shakes_cleaned.csv"
    }

    datasets = load_data(files)
    print("Datasets loaded successfully!")

    category = "Protein Bars"
    query = "Which are the top 3 protein products with the highest protein content?"
    
    if category not in datasets:
        print(f"Error: Category '{category}' not found in datasets.")
        exit(1)
    
    filtered_data = query_data(datasets[category], query)
    # print(filtered_data.head())  # Debugging: Check filtered results
    response = generate_response(filtered_data, query)
    print("\n--- Generated Response ---")
    print(response)
