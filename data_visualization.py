import pandas as pd
import matplotlib.pyplot as plt

def load_data(filename: str) -> pd.DataFrame:
    """
    Load cleaned CSV data into a DataFrame.
    
    Args:
        filename (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    return pd.read_csv(filename)

def plot_energy_vs_protein(df: pd.DataFrame, category: str):
    """
    Scatter plot of Energy (kcal) vs. Protein content.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        category (str): Name of the product category for labeling.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(df['energy_kcal'], df['protein_100g'], alpha=0.7, c='blue')
    plt.title(f'Energy vs. Protein Content ({category})')
    plt.xlabel('Energy (kcal per 100g)')
    plt.ylabel('Protein (g per 100g)')
    plt.grid(True)
    plt.savefig(f'{category}_energy_vs_protein.png')
    plt.show()

def plot_price_vs_protein(df: pd.DataFrame, category: str):
    """
    Scatter plot of Price vs. Protein content.
    """
    plt.scatter(df['price'], df['protein_100g'], alpha=0.7, c='blue')
    plt.title(f'Price vs. Protein Content ({category})')
    plt.xlabel('Price ($)')
    plt.ylabel('Protein (g per 100g)')
    plt.show()

def plot_macronutrient_distribution(df: pd.DataFrame, category: str):
    """
    Histograms for macronutrient distribution (protein, fat, carbs).
    
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        category (str): Name of the product category for labeling.
    """
    nutrients = ['protein_100g', 'fat_100g', 'carbohydrates_100g']
    df[nutrients].hist(bins=15, figsize=(12, 6), alpha=0.7)
    plt.suptitle(f'Macronutrient Distribution ({category})')
    plt.savefig(f'{category}_macronutrient_distribution.png')
    plt.show()

def plot_allergen_frequency(df: pd.DataFrame, category: str):
    """
    Bar chart of allergen frequencies.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        category (str): Name of the product category for labeling.
    """
    allergen_counts = df['allergens'].value_counts()
    allergen_counts = allergen_counts[allergen_counts.index != "None"]  # Exclude products with no allergens

    plt.figure(figsize=(10, 6))
    allergen_counts.plot(kind='bar', color='orange', alpha=0.8)
    plt.title(f'Allergen Frequency ({category})')
    plt.xlabel('Allergen')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{category}_allergen_frequency.png')
    plt.show()

if __name__ == "__main__":
    # File paths for the cleaned data
    files = {
        "Healthy Breakfast": "healthy_breakfast_cleaned.csv",
        "Protein Bars": "protein_bars_cleaned.csv",
        "Protein Cookies": "protein_cookies_cleaned.csv"
    }

    for category, file in files.items():
        print(f"Visualizing data for {category}...")
        data = load_data(file)
        
        # Drop rows with missing values for visual clarity
        data = data.dropna(subset=['energy_kcal', 'protein_100g', 'fat_100g', 'carbohydrates_100g'])
        
        # Generate visualizations
        plot_energy_vs_protein(data, category)
        plot_macronutrient_distribution(data, category)
        plot_allergen_frequency(data, category)
