import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="IMDb Movies Dashboard", layout="wide")
st.title("🎬 IMDb Movies Dashboard")
st.markdown(
    "Interactive dashboard for exploring IMDb movie ratings, genres and trends over time."
)

df = pd.read_csv("./data/imdb_top_1000.csv")

# -----------------------------
# Data preparation
# -----------------------------
# Rename columns for consistency (dataset-dependent, but common ones)
df.columns = [c.lower().strip() for c in df.columns]

# Ensure numeric columns
df["imdb_rating"] = pd.to_numeric(df["imdb_rating"], errors="coerce")
df["released_year"] = pd.to_numeric(df["released_year"], errors="coerce")
df["runtime"] = (
    df["runtime"]
    .str.replace(" min", "", regex=False)
    .astype(float)
)

# Drop rows with essential missing values
df = df.dropna(subset=["imdb_rating", "released_year", "genre"])

# Split genres (keep first genre for simplicity)
df["main_genre"] = df["genre"].str.split(",").str[0]

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

genres = sorted(df["main_genre"].unique())
selected_genres = st.sidebar.multiselect(
    "Select genre(s)", genres, default=genres
)

year_min, year_max = int(df["released_year"].min()), int(df["released_year"].max())
selected_years = st.sidebar.slider(
    "Release year range", year_min, year_max, (year_min, year_max)
)

rating_min, rating_max = float(df["imdb_rating"].min()), float(df["imdb_rating"].max())
selected_ratings = st.sidebar.slider(
    "IMDb rating range", rating_min, rating_max, (rating_min, rating_max)
)

# Apply filters
df_filtered = df[
    (df["main_genre"].isin(selected_genres)) &
    (df["released_year"].between(*selected_years)) &
    (df["imdb_rating"].between(*selected_ratings))
]

# -----------------------------
# Visualization 1: Rating over time
# -----------------------------
st.subheader("📈 Average IMDb Rating Over Time")

ratings_by_year = (
    df_filtered
    .groupby("released_year")["imdb_rating"]
    .mean()
    .reset_index()
)

fig_time = px.line(
    ratings_by_year,
    x="released_year",
    y="imdb_rating",
    labels={
        "released_year": "Release Year",
        "imdb_rating": "Average IMDb Rating",
    },
    markers=True,
)

st.plotly_chart(fig_time, width='stretch')

# -----------------------------
# Visualization 2: Ratings by genre
# -----------------------------
st.subheader("🎭 IMDb Rating Distribution by Genre")

fig_genre = px.box(
    df_filtered,
    x="main_genre",
    y="imdb_rating",
    labels={
        "main_genre": "Genre",
        "imdb_rating": "IMDb Rating",
    },
)

st.plotly_chart(fig_genre, width='stretch')

# -----------------------------
# Visualization 3: Runtime vs rating
# -----------------------------
st.subheader("⏱️ Runtime vs IMDb Rating")

fig_scatter = px.scatter(
    df_filtered,
    x="runtime",
    y="imdb_rating",
    color="main_genre",
    labels={
        "runtime": "Runtime (minutes)",
        "imdb_rating": "IMDb Rating",
    },
    opacity=0.7,
)

st.plotly_chart(fig_scatter, width='stretch')

# -----------------------------
# Insights
# -----------------------------
st.subheader("📌 Key Insights")

best_genre = (
    df_filtered
    .groupby("main_genre")["imdb_rating"]
    .mean()
    .idxmax()
)

best_decade = (
    (df_filtered["released_year"] // 10 * 10)
    .value_counts()
    .idxmax()
)

st.markdown(
    f"""
- **Best rated genre (on average):** {best_genre}
- **Decade with most movies in the dataset:** {best_decade}s
- **Number of movies analysed:** {len(df_filtered)}
"""
)
