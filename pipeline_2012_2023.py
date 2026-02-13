import pandas as pd
import unicodedata
import re
from typing import List

YEARS = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
DATA_PATH = "data"
OUTPUT_FILE = "data/lic_clean_2012_2023.csv"
AGE_GROUPS_NEW = {
    "1_9": ["1 à 4 ans", "5 à 9 ans"],
    "10_19": ["10 à 14 ans", "15 à 19 ans"],
    "20_29": ["20 à 24 ans", "25 à 29 ans"],
    "30_59": ["30 à 34 ans", "35 à 39 ans","40 à 44 ans", "45 à 49 ans","50 à 54 ans", "55 à 59 ans"],
    "60_74": ["60 à 64 ans", "65 à 69 ans","70 à 74 ans"],
    "75": ["75 à 79 ans", "80 ans et plus"],
}

# BOTH
def clean_columns(df):
    df.columns = [col.lstrip("\ufeff") for col in df.columns]  # enlève BOM si présent (fichier 2012)
    df = df.rename(columns=lambda x: re.sub(r"_\d{4}$", "", str(x)))
    
    df.columns = (
        df.columns
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace("_-_", "_", regex=False)
    )
    return df

# BOTH 
def add_year(df, year: int):
    df["annee"] = year
    return df

# OLD
def import_dept_num(df):
    communes_dept = pd.read_csv("data/recap_communes_par_departement.csv")
    communes_dept = communes_dept.rename(columns={"Département":"num_departement","Code Commune":"code_commune"})
    df = df.merge(communes_dept,how="inner",on="code_commune")

    return df

# OLD
def rename_columns_2012_2018(df):

    synonyms = {
        "nom_commune": ["libelle", "libgeo"],
        "code_fed": ["fed"],
        "code_commune": ["newcog2", "cog2"],
        "nom_fed": ["federation"],
        "total_lic": ["l"],
        "total_f": ["l_f"],
        "total_h": ["l_h"],
    }

    rename_map = {}

    for new_name, possible_names in synonyms.items():
        for col in possible_names:
            if col in df.columns:
                rename_map[col] = new_name

    df = df.rename(columns=rename_map)

    return df

# NEW
def rename_columns_2019_2023(df):
    rename_map = {"code commune":"code_commune",
                  "commune":"nom_commune",
                  "departement":"num_departement",
                  "code":"code_fed",
                  "federation":"nom_fed",
                  "total":"total_lic"}
    return df.rename(columns=rename_map)

# BOTH
def clean_federation_name(text):
    if pd.isna(text):
        return text
    
    # 1️⃣ mettre en majuscules
    text = text.upper()
    
    # 2️⃣ enlever accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    # 3️⃣ supprimer FF, DE, D'
    text = re.sub(r"\bFF\b", "", text)
    text = re.sub(r"\bDE\b", "", text)
    text = re.sub(r"\bD['’]", "", text)  # gère ' et ’
    text = re.sub(r"\bDES\b", "", text)
    text = re.sub(r"\bDU\b", "", text)
    text = re.sub(r"\bF\b", "", text)
    text = re.sub(r"\bFEDERATION FRANCAISE\b", "", text)

    
    # 4️⃣ enlever espaces multiples
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

# BOTH
def clean_federation(df):
    if "nom_fed" in df.columns:
        df["nom_fed"] = df["nom_fed"].apply(clean_federation_name)
    return df

# NEW
def format_departement(df):
    df["num_departement"] = df["num_departement"].astype(str).str.zfill(2)
    return df

# NEW
def compute_totals_2019_2023(df):
    f_cols = [col for col in df.columns if col.startswith("f_")]
    h_cols = [col for col in df.columns if col.startswith("h_")]

    df["total_f"] = df[f_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    df["total_h"] = df[h_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    df["total_lic"] = df["total_f"] + df["total_h"]

    return df

# OLD
def compute_age_categories_2012_2018(df):
    age_mapping = {
        "1_9": ["0_4", "5_9"],
        "10_19": ["10_14", "15_19"],
        "20_29": ["20_29"],
        "30_59": ["30_44", "45_59"],
        "60_74": ["60_74"],
        "75": ["75", "75_99"]  # <- inclure 75_99 si présent
    }
    

    for sex in ["f", "h"]:
        for new_cat, source_cats in age_mapping.items():
            cols = [f"l_{age}_{sex}" for age in source_cats if f"l_{age}_{sex}" in df.columns]
            if cols:  # s'assure qu'il y a au moins une colonne
                df[f"{sex}_{new_cat}"] = df[cols].sum(axis=1)
            else:
                df[f"{sex}_{new_cat}"] = 0  # si aucune colonne, mettre 0
    return df

# NEW
def compute_age_categories_2019_2023(df):
    for prefix in ["f", "h"]:
        for group, ages in AGE_GROUPS_NEW.items():

            cols = [
                f"{prefix}_{age}"
                .replace("à", "a")
                .replace(" ", "_")
                for age in ages
            ]

            cols = [col for col in cols if col in df.columns]

            df[f"{prefix}_{group}"] = (
                df[cols]
                .apply(pd.to_numeric, errors="coerce")
                .sum(axis=1)
                if cols else 0
            )

    return df

# OLD
def import_region(df):
    # import file departements-france to get code-region
    dept = pd.read_csv("data/departements-france.csv")

    # transfo columns types and name
    dept = dept.rename(columns=({"code_departement":"num_departement"}))
    dept["num_departement"] = dept["num_departement"].astype(str)
    df["num_departement"] = df["num_departement"].astype(str)

    # Merge 2 datasets
    df = df.merge(dept,on="num_departement",how="left")

    # Cleaning
    df = df.drop(columns=["region","nom_departement","code_region"],errors="ignore")
    df = df.rename(columns={"nom_region": "region"})

    return df


# BOTH
def reorder_columns(df):
    ordered_cols = [
        "annee",
        "code_commune",
        "nom_commune",
        "num_departement",
        "region",
        "code_fed",
        "nom_fed",
        "total_lic",
        "total_f",
        "total_h",
        "h_1_9",
        "h_10_19",
        "h_20_29",
        "h_30_59",
        "h_60_74",
        "h_75",
        "f_1_9",
        "f_10_19",
        "f_20_29",
        "f_30_59",
        "f_60_74",
        "f_75",
    ]
    if "region" not in df.columns:
        df["region"] = None  # ou une valeur par défaut

    # Ne garder que les colonnes existantes
    cols_to_use = [c for c in ordered_cols if c in df.columns]
    return df[cols_to_use]

def transform_lic_file(year: int):
    print(f"Processing year {year}...")

    # Les années antérieures à 2015 ont des encodages différents :
    file_path = f"{DATA_PATH}/lic-data-{year}.csv"
    if year <= 2015:
        df = pd.read_csv(file_path, low_memory=False, encoding="utf-8-sig")
    elif year >= 2019:
        df = pd.read_csv(file_path, sep=";", low_memory=False, encoding="utf-8")
    else:
        df = pd.read_csv(file_path, sep=";", encoding="latin1", low_memory=False)

    df = clean_columns(df)
    df = add_year(df, year)

    # Renommage des colonnes et calculs:
    if year <= 2018:
        df = rename_columns_2012_2018(df)
        df = import_dept_num(df)
        df = compute_age_categories_2012_2018(df)
    else:
        df = rename_columns_2019_2023(df)
        df = format_departement(df)
        df = compute_totals_2019_2023(df)
        df = compute_age_categories_2019_2023(df)
          
    # Les années antérieures à 2014 n'ont pas de région
    if year <= 2014:
        df = import_region(df)

    df = clean_federation(df)    
    df = reorder_columns(df)

    return df

if __name__ == "__main__":
    all_data = pd.concat(
        [transform_lic_file(year) for year in YEARS],
        ignore_index=True
    )

    all_data.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Fichier final généré : {OUTPUT_FILE}")
