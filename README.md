# Jedha DAFS Final Project – French Sports Licenses & Population Dashboard

**Exploratory data analysis, ETL, AWS database integration, and interactive Streamlit dashboard**  
Final project for the **Data Analyst Full-Stack (DAFS)** bootcamp at Jedha.

This project analyzes sports license data in France (2019–2023), combines it with regional population statistics, performs data transformation & cleaning, queries additional data from an AWS-hosted database, and exposes interactive visualizations via a Streamlit web app.

## ✨ Features

- ETL pipeline transforming raw license data (2019–2023)
- Exploratory Data Analysis (notebooks) on sports licenses evolution
- Connection to AWS database (AURORA RDS MySQL) using credentials from `.env`
- SQL queries for licenses, medias, clubs stored securely in `.env`
- Interactive Streamlit dashboard showing:
  - Rolling averages & totals of licenses
  - Regional breakdowns (with geo-visualization using GeoJSON)
  - Population-normalized metrics
- Basic ML functions preparation (future extension possible)

## 🛠️ Tech Stack

- **Python** 3.9+
- **Data processing** — pandas, numpy
- **Visualization** — Streamlit, plotly / matplotlib / seaborn (in notebooks)
- **Database** — AWS (Redshift or similar) via psycopg2 / sqlalchemy + boto3 possible
- **Geospatial** — GeoPandas or folium/plotly + regions.geojson
- **Environment** — dotenv for secrets (.env)

## 📁 Project Structure
JedhaProject/

├── Machine_Learning/           # ML experiments / functions

├── Streamlit_project_jedha/    # Streamlit pages / modules

├── pages/                      # Additional Streamlit pages

├── .streamlit/                 # Streamlit config

├── eda_licences.ipynb          # Main EDA notebook

├── eda_licences_V2.ipynb       # Improved / alternative EDA

├── DBConnector.py              # AWS DB connection + query loader from .env

├── streamlit_app.py            # Main Streamlit entry point

├── streamlit_graphs.py         # Graph utilities

├── streamlit_lics.py           # License-specific dashboard logic

├── ML_function.py              # Machine learning helpers

├── transfo_2019_2023.py        # Data transformation script (2019–2023)

├── utils.py                    # Shared utilities

├── requirements.txt

├── Dockerfile                  # Optional containerization

├── pop_by_region.csv           # Population data by French region

├── regions.geojson             # GeoJSON for French regions

└── .env.example                # Template – create your own .env !


**Important note about data files (.csv / .xls / .xlsx)**  
Most raw Excel/CSV files are **not** directly loaded in the final app (they were used during EDA & transformation phases).  
The dashboard mainly pulls cleaned/transformed data + live queries from the **AWS database**.

## 🚀 Quick Start (Local)

1. Clone the repo
   ```bash
   git clone https://github.com/valendrenitos/JedhaProject.git
   cd JedhaProject

2.  Create virtual environment
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

3.  Install dependencies
pip install -r requirements.txt

4. Create .env file in the root (never commit it!)

# Example .env – replace with your real AWS credentials
DB_HOST=your-redshift-cluster.xxx.eu-west-1.redshift.amazonaws.com
DB_PORT=5439
DB_NAME=dev
DB_USER=your_user
DB_PASSWORD=SuperSecret123!

queryLicenses=SELECT * FROM licenses_table LIMIT 100
queryMedias=SELECT ... FROM medias ...
queryClubs=SELECT ... FROM clubs ...

5. Run the Streamlit app
streamlit run streamlit_app.py

# Roadmap / What could be improved
Integrate more raw XLS/CSV files directly as fallback when AWS is down
Add caching (st.cache_data / st.cache_resource) for faster dashboard
Deploy to Streamlit Community Cloud or AWS EC2
More advanced ML (clustering federations, prediction of license growth…)
Tests & better error handling on DB connection


