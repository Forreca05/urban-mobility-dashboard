# IMDb Movies Dashboard

Interactive dashboard for exploratory data analysis and visualization of IMDb movies data.
The project focuses on understanding trends in movie ratings, genres and release years.

## Tech Stack
- Python
- Pandas
- Plotly
- Streamlit

## Dataset
The dataset used in this project is:
- **IMDb Dataset of Top 1000 Movies and TV Shows**
- Source: Kaggle

It includes information such as movie title, release year, genre, IMDb rating and duration.

## Project Structure
app/        # Streamlit application
data/       # Dataset files

## Setup
```bash
git clone https://github.com/your-username/imdb-movies-dashboard.git
cd imdb-movies-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/dashboard.py
da