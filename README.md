# TMDB Movie Explorer

An interactive Streamlit dashboard built using the **TMDB 5000 Movie Dataset**. This project provides visual storytelling insights into global movie trends based on genres, budgets, revenues, languages, and more.

## Features

* **Filter by year, genre, and revenue** using an intuitive sidebar
* **Visualize genre trends** using bar and pie charts
* **Compare budget vs. revenue** with optional log scale
* **Explore movie release patterns over time** and overlay with popularity
* **Analyze revenue distribution by genre** with box plots
* **Discover dominant spoken languages and production countries**
* **Summary section** to highlight key insights

## Visuals Included

* Bar Chart: Most Common Genres
* Pie Chart: Genre Distribution (Top 6 + Other)
* Scatter Plot: Budget vs. Revenue (with log scale toggle)
* Line Chart: Number of Movies Released Over Time
* Box Plot: Revenue by Genre
* Bar Charts: Spoken Languages and Production Countries

## Key Insights

* **Action, Drama, and Comedy** dominate in terms of production volume.
* **Sci-Fi and Adventure** genres show higher revenue distributions.
* The early **2000s saw a boom** in movie releases, likely due to digital filmmaking.
* **English** remains the most common language, but global diversity is rising.
* Some **low-budget movies achieve extremely high revenue**, showing strong ROI.

## How to Run

1. Make sure you have Python and Streamlit installed:

```bash
pip install streamlit pandas seaborn matplotlib
```

2. Place `tmdb_dashboard.py` and `tmdb_5000_movies.csv` in the same directory.

3. Run the Streamlit app:

```bash
streamlit run tmdb_dashboard.py
```

## Files

* `tmdb_dashboard.py`: Main Streamlit app
* `tmdb_5000_movies.csv`: Dataset file (from Kaggle)

## Dataset Source

[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)


## License

MIT License. This project is for educational and portfolio use.
