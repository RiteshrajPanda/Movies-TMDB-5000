import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ast

# Page config
st.set_page_config(page_title="TMDB Movie Explorer", layout="wide")

# Title
st.title("TMDB Movie Explorer")
st.markdown("Explore visual trends from 5000 movies in the TMDB dataset, including genre, revenue, popularity, and more.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("tmdb_5000_movies.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    df['genres'] = df['genres'].apply(ast.literal_eval)
    df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in x])
    return df

df = load_data()

# Genre list for sidebar
all_genres = sorted(list({genre for sublist in df['genres'] for genre in sublist}))

# Sidebar filters
st.sidebar.header("Filter Options")
year_range = st.sidebar.slider("Release Year", 1980, 2020, (2000, 2015))
selected_genres = st.sidebar.multiselect("Select Genres", all_genres, default=all_genres[:3])
min_revenue = st.sidebar.slider("Minimum Revenue ($M)", 0, 1000, 100)

# Filter dataset
df_filtered = df[(df['release_year'].between(*year_range)) &
                 (df['revenue'] > min_revenue * 1e6) &
                 (df['genres'].apply(lambda g: any(genre in g for genre in selected_genres)))]

# Genre Distribution
st.subheader("Most Common Genres")
from collections import Counter

flat_genres = [genre for sublist in df_filtered['genres'] for genre in sublist]
genre_counts = pd.Series(Counter(flat_genres)).sort_values(ascending=False).head(10)
genre_df = genre_counts.reset_index()
genre_df.columns = ['Genre', 'Count']

fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=genre_df, x='Count', y='Genre', palette='viridis', ax=ax1)
ax1.set_title("Top 10 Genres")
st.pyplot(fig1)

# Budget vs Revenue
st.subheader("Budget vs Revenue")
scatter_data = df_filtered[(df_filtered['budget'] > 0) & (df_filtered['revenue'] > 0)].copy()
scatter_data['ROI'] = scatter_data['revenue'] / scatter_data['budget']

use_log = st.checkbox("Use Log Scale")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=scatter_data, x='budget', y='revenue', hue='ROI', palette='coolwarm', ax=ax2)
if use_log:
    ax2.set_xscale('log')
    ax2.set_yscale('log')
ax2.set_title("Budget vs Revenue")
st.pyplot(fig2)

# Release Trends
st.subheader("Release Trends Over Time")
trend = df_filtered.groupby('release_year').agg({'title': 'count', 'popularity': 'mean'}).rename(columns={'title': 'movie_count'})
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(trend.index, trend['movie_count'], color='blue', label='Movies Released')
ax3.set_ylabel("Movie Count", color='blue')
ax4 = ax3.twinx()
ax4.plot(trend.index, trend['popularity'], color='green', linestyle='--', label='Avg Popularity')
ax4.set_ylabel("Avg Popularity", color='green')
ax3.set_title("Movies Released per Year and Popularity")
st.pyplot(fig3)

# Revenue by Genre
st.subheader("Revenue by Genre")
df_rev = df_filtered[df_filtered['revenue'] > 0].copy()
df_rev = df_rev.explode('genres').rename(columns={'genres': 'genre'})
fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df_rev, x='genre', y='revenue', showfliers=False, ax=ax4)
ax4.set_yscale('log')
ax4.set_title("Revenue Distribution by Genre")
ax4.set_xlabel("Genre")
ax4.set_ylabel("Revenue (log scale)")
plt.xticks(rotation=45)
st.pyplot(fig4)

# Language & Country Diversity
st.subheader("Language & Country Diversity")
df['spoken_languages'] = df['spoken_languages'].apply(ast.literal_eval)
languages = [lang['name'] for sublist in df['spoken_languages'] for lang in sublist]
lang_counts = pd.Series(Counter(languages)).sort_values(ascending=False).head(10)
lang_df = lang_counts.reset_index()
lang_df.columns = ['Language', 'Count']
fig5, ax5 = plt.subplots(figsize=(8, 5))
sns.barplot(data=lang_df, x='Count', y='Language', palette='mako', ax=ax5)
ax5.set_title("Top 10 Spoken Languages")
st.pyplot(fig5)

# Conclusion
st.subheader("Summary")
st.markdown("""
- **From 1980 to 2020**
- **Action, Adventure, and Thriller** are the most common genres.
- **High-budget movies** tend to earn more, but several **low-budget films** show great ROI.
- **2000s** saw a sharp rise in movie production.
- **Sci-Fi, Fantasy and Adventure** genres tend to have higher revenue distributions.
- English dominates spoken languages, but **global diversity is rising**.
""")