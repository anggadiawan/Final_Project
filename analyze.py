import pandas as pd
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from matplotlib.cm import get_cmap
from itertools import cycle

# Define file paths for the datasets
file_paths = {
    "Structures": "Structures_data.csv",
    "Engineering Structures": "Engineering_Structures_data.csv",
    "Building and Environment": "Building_and_Environment_data.csv"
}

# Define stopwords and preprocess function
stop_words = set(stopwords.words('english'))

def preprocess_title(title):
    if pd.isna(title):
        return []
    tokens = word_tokenize(title.lower())  # Tokenize and lowercase
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Remove stopwords
    return filtered_tokens

# Define keywords for themes, sub-themes, and sub-sub-themes
theme_keywords = {
    'Numerical Investigation': ['finite', 'element', 'simulation', 'numerical', 'analysis', 'optimization'],
    'Experimental Investigation': ['experimental', 'test', 'physical', 'laboratory', 'measurement'],
    'Hybrid Methods': ['hybrid', 'combined', 'integration']
}

subtheme_keywords = {
    'Performance Analysis': ['performance', 'behavior', 'response', 'stiffness', 'strength', 'durability'],
    'Optimization': ['optimization', 'design', 'efficiency'],
    'Material Behavior': ['material', 'properties', 'composite', 'steel', 'concrete', 'frp'],
    'Construction Techniques': ['construction', 'technique', 'methodology', 'approach'],
    'Damage and Retrofitting': ['damage', 'retrofitting', 'repair', 'rehabilitation'],
    'Design Methods': ['design', 'method', 'strut', 'tie']
}

subsubtheme_keywords = {
    'Concrete': ['concrete', 'cement'],
    'Steel': ['steel', 'metal'],
    'FRP': ['fiber', 'reinforced', 'composite'],
    'Bridges': ['bridge', 'bridges'],
    'Buildings': ['building', 'buildings'],
    'Earthquake Loads': ['earthquake', 'seismic'],
    'Wind Loads': ['wind'],
    'Fire Resistance': ['fire', 'resistance']
}

def categorize_title(tokens):
    theme = None
    subtheme = None
    subsubtheme = None

    # Identify theme
    for key, keywords in theme_keywords.items():
        if any(word in tokens for word in keywords):
            theme = key
            break

    # Identify sub-theme
    for key, keywords in subtheme_keywords.items():
        if any(word in tokens for word in keywords):
            subtheme = key
            break

    # Identify sub-sub-theme
    for key, keywords in subsubtheme_keywords.items():
        if any(word in tokens for word in keywords):
            subsubtheme = key
            break

    return theme, subtheme, subsubtheme

# Load and preprocess data for all journals
def load_and_preprocess(file_paths):
    combined_data = []
    for journal, path in file_paths.items():
        # Load dataset
        data = pd.read_csv(path)

        # Add journal name column
        data['journal'] = journal

        # Extract year from DOI
        data['year'] = data['doi'].str.extract(r'(?<=\.)(\d{4})(?=\.)')
        data['year'] = pd.to_numeric(data['year'], errors='coerce')

        # Preprocess titles
        data['processed_title'] = data['title'].apply(preprocess_title)

        # Apply theme, subtheme, and subsubtheme categorization
        data[['theme', 'subtheme', 'subsubtheme']] = data['processed_title'].apply(
            lambda tokens: pd.Series(categorize_title(tokens))
        )

        combined_data.append(data)
    return pd.concat(combined_data, ignore_index=True)

# Combine all datasets and preprocess
combined_data = load_and_preprocess(file_paths)
cleaned_data = combined_data.dropna(subset=['theme', 'subtheme', 'subsubtheme', 'year'])

def get_color_map(categories):
    cmap = get_cmap("tab20")  # Choose a color map
    colors = cycle(cmap.colors)  # Create a cycle of colors
    return {category: next(colors) for category in sorted(categories)}

# Define the color maps based on unique categories in the data
unique_themes = cleaned_data['theme'].dropna().unique()
unique_subthemes = cleaned_data['subtheme'].dropna().unique()
unique_subsubthemes = cleaned_data['subsubtheme'].dropna().unique()

theme_colors = get_color_map(unique_themes)
subtheme_colors = get_color_map(unique_subthemes)
subsubtheme_colors = get_color_map(unique_subsubthemes)

# Function: Area Chart for Themes, Subthemes, and Subsubthemes per Journal
def plot_area_charts(data):
    journals = data['journal'].unique()

    for journal in journals:
        journal_data = data[data['journal'] == journal]

        # Aggregate data for themes, subthemes, and subsubthemes
        theme_year_counts = journal_data.groupby(['year', 'theme']).size().reset_index(name='count')
        subtheme_year_counts = journal_data.groupby(['year', 'subtheme']).size().reset_index(name='count')
        subsubtheme_year_counts = journal_data.groupby(['year', 'subsubtheme']).size().reset_index(name='count')

        # Create pivot tables
        pivot_theme = theme_year_counts.pivot(index='year', columns='theme', values='count').fillna(0)
        pivot_subtheme = subtheme_year_counts.pivot(index='year', columns='subtheme', values='count').fillna(0)
        pivot_subsubtheme = subsubtheme_year_counts.pivot(index='year', columns='subsubtheme', values='count').fillna(0)

        # Set up the matplotlib figure
        fig, axes = plt.subplots(3, 1, figsize=(14, 18), sharex=True)

        # Plot Themes
        pivot_theme.plot(kind='area', stacked=True, alpha=0.7, ax=axes[0], color=[theme_colors[col] for col in pivot_theme.columns])
        axes[0].set_title(f'Themes Over the Years ({journal})', fontsize=16)
        axes[0].set_ylabel('Number of Entries', fontsize=12)
        axes[0].legend(title='Themes', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Plot Subthemes
        pivot_subtheme.plot(kind='area', stacked=True, alpha=0.7, ax=axes[1], color=[subtheme_colors[col] for col in pivot_subtheme.columns])
        axes[1].set_title(f'Subthemes Over the Years ({journal})', fontsize=16)
        axes[1].set_ylabel('Number of Entries', fontsize=12)
        axes[1].legend(title='Subthemes', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Plot Subsubthemes
        pivot_subsubtheme.plot(kind='area', stacked=True, alpha=0.7, ax=axes[2], color=[subsubtheme_colors[col] for col in pivot_subsubtheme.columns])
        axes[2].set_title(f'Subsubthemes Over the Years ({journal})', fontsize=16)
        axes[2].set_xlabel('Year', fontsize=12)
        axes[2].set_ylabel('Number of Entries', fontsize=12)
        axes[2].legend(title='Subsubthemes', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()

# Function: Stacked Bar Chart for Themes and Subthemes by Year per Journal
def plot_stacked_bars(data):
    journals = data['journal'].unique()

    for journal in journals:
        journal_data = data[data['journal'] == journal]
        stacked_data = journal_data.groupby(['year', 'subtheme', 'theme']).size().reset_index(name='count')
        unique_years = sorted(stacked_data['year'].unique())

        fig, axes = plt.subplots(len(unique_years), 1, figsize=(14, len(unique_years) * 5), sharex=False)

        for i, year in enumerate(unique_years):
            year_data = stacked_data[stacked_data['year'] == year]
            pivot_data = year_data.pivot_table(
                index='subtheme',
                columns='theme',
                values='count',
                aggfunc='sum'
            ).fillna(0)
            pivot_data = pivot_data.loc[pivot_data.sum(axis=1).sort_values(ascending=False).index]

            pivot_data.plot(
                kind='bar',
                stacked=True,
                ax=axes[i],
                color=[theme_colors[col] for col in pivot_data.columns],
                alpha=0.85
            )

            axes[i].set_title(f'Research Area vs Number of Articles ({year}) - {journal}', fontsize=16)
            axes[i].set_ylabel('Number of Articles', fontsize=12)
            axes[i].tick_params(axis='x', rotation=45)
            axes[i].legend(title='Themes', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()

# Function: Stacked Bar Chart for Subthemes and Subsubthemes by Year per Journal
def plot_subtheme_subsubtheme_bars(data):
    journals = data['journal'].unique()

    for journal in journals:
        journal_data = data[data['journal'] == journal]
        stacked_data = journal_data.groupby(['year', 'subsubtheme', 'subtheme']).size().reset_index(name='count')
        unique_years = sorted(stacked_data['year'].unique())

        fig, axes = plt.subplots(len(unique_years), 1, figsize=(14, len(unique_years) * 5), sharex=False)

        for i, year in enumerate(unique_years):
            year_data = stacked_data[stacked_data['year'] == year]
            pivot_data = year_data.pivot_table(
                index='subsubtheme',
                columns='subtheme',
                values='count',
                aggfunc='sum'
            ).fillna(0)
            pivot_data = pivot_data.loc[pivot_data.sum(axis=1).sort_values(ascending=False).index]

            pivot_data.plot(
                kind='bar',
                stacked=True,
                ax=axes[i],
                color=[subtheme_colors[col] for col in pivot_data.columns],
                alpha=0.85
            )

            axes[i].set_title(f'Research Detail vs Number of Articles ({year}) - {journal}', fontsize=16)
            axes[i].set_ylabel('Number of Articles', fontsize=12)
            axes[i].tick_params(axis='x', rotation=45)
            axes[i].legend(title='Subthemes', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()

# Generate all charts for each journal
plot_area_charts(cleaned_data)
plot_stacked_bars(cleaned_data)
plot_subtheme_subsubtheme_bars(cleaned_data)