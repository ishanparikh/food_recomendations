import streamlit as st
import pandas as pd
from llm_integration import load_data, query_data, generate_response

import matplotlib.pyplot as plt

def plot_protein_vs_price(df: pd.DataFrame, category: str):
    """
    Scatter plot of Protein vs. Price.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(df['price'], df['protein_100g'], alpha=0.7, c='blue')
    plt.title(f'Protein vs. Price in {category}')
    plt.xlabel('Price ($)')
    plt.ylabel('Protein (g per 100g)')
    plt.grid(True)
    st.pyplot(plt)

def plot_macronutrient_distribution(df: pd.DataFrame, category: str):
    """
    Histograms for Macronutrient Distribution.
    """
    nutrients = ['protein_100g', 'fat_100g', 'carbohydrates_100g']
    df[nutrients].hist(bins=15, figsize=(10, 6), alpha=0.7)
    plt.suptitle(f'Macronutrient Distribution ({category})')
    st.pyplot(plt)


# Load datasets
files = {
    "Healthy Breakfast": "healthy_breakfast_cleaned.csv",
    "Protein Bars": "protein_bars_cleaned.csv",
    "Protein Cookies": "protein_cookies_cleaned.csv",
    "Protein Snacks": "protein_snacks_cleaned.csv",
    "Protein Shakes": "protein_shakes_cleaned.csv"
}
datasets = load_data(files)

# Streamlit app interface
st.title("Protein Product Query Interface 🍫")

# Select category
category = st.selectbox("Select a category", list(files.keys()))

# Input query
query = st.text_input("Enter your query (e.g., highest protein, gluten-free):")

# Search button
if st.button("Search"):
    if category not in datasets:
        st.error(f"Category '{category}' not found.")
    else:
        # Filter data
        filtered_data = query_data(datasets[category], query)
        
        # Show filtered data
        st.subheader("Filtered Results")
        if filtered_data.empty:
            st.warning("No matching data found.")
        else:
            st.dataframe(filtered_data)

            # Visualizations
            st.subheader("Visualizations")
            st.write("### Protein vs. Price")
            plot_protein_vs_price(filtered_data, category)
            st.write("### Macronutrient Distribution")
            plot_macronutrient_distribution(filtered_data, category)

        # Generate response using LLM
        st.subheader("LLM Response")
        response = generate_response(filtered_data, query)
        st.write(response)
