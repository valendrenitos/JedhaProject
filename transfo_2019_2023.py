import pandas as pd
import unicodedata
import re

YEARS = [2019, 2020, 2021, 2022, 2023]
DATA_PATH = "data"
OUTPUT_FILE = "data/lic_clean_2019_2023.csv"

AGE_GROUPS = {
    "1_9": ["1 à 4 ans", "5 à 9 ans"],
    "10_19": ["10 à 14 ans", "15 à 19 ans"],
    "20_29": ["20 à 24 ans", "25 à 29 ans"],
    "30_59": ["30 à 34 ans","35 à 39 ans", "40 à 44 ans", "45 à 49 ans","50 à 54 ans","55 à 59 ans"],
    "60_74": ["60 à 64 ans","65 à 69 ans","70 à 74 ans"],
    "75": ["75 à 79 ans","80 à 99 ans"]
}

def clean_columns(df):
    df.columns = (
        df.columns
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df

def add_year(df, year: int):
    df["annee"] = year
    return df

def rename_columns(df):
    rename_map = {"code commune":"code_commune",
                  "commune":"nom_commune",
                  "departement":"num_departement",
                  "code":"code_fed",
                  "federation":"nom_fed",
                  "total":"total_lic"}
    return df.rename(columns=rename_map)

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

    
    # 4️⃣ enlever espaces multiples
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def clean_federation(df):
    df["nom_fed"] = df["nom_fed"].apply(clean_federation_name)
    return df

def format_departement(df):
    df["num_departement"] = df["num_departement"].astype(str).str.zfill(2)
    return df

def compute_totals(df):
    f_cols = [col for col in df.columns if col.startswith("F - ")]
    h_cols = [col for col in df.columns if col.startswith("H - ")]

    df["total_f"] = df[f_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    df["total_h"] = df[h_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    df["total_lic"] = df["total_f"] + df["total_h"]

    return df

def compute_age_categories(df):
    for prefix in ["f", "h"]:
        for group, ages in AGE_GROUPS.items():

            # reconstruire les noms EXACTS après clean_columns
            cols = [
                f"{prefix}_-_{age}"
                .replace("à", "a")
                .replace(" ", "_")
                for age in ages
            ]

            # garder uniquement celles présentes dans le df
            cols = [col for col in cols if col in df.columns]

            df[f"{prefix}_{group}"] = (
                df[cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
                if cols else 0
            )

    return df

def drop_unused_columns(df):
    cols_to_drop = [col for col in df.columns if "-" in col]
    return df.drop(columns=cols_to_drop)

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
    return df[ordered_cols]

# =========================
# Pipeline
# =========================

def transform_lic_file(year: int):
    print(f"Processing year {year}...")

    file_path = f"{DATA_PATH}/lic-data-{year}.csv"
    #df = pd.read_csv(file_path, sep=";")
    df = pd.read_csv(file_path, sep=";", low_memory=False)
    df = clean_columns(df)
    df = add_year(df, year)
    df = rename_columns(df)
    df = clean_federation(df)
    df = format_departement(df)
    df = compute_totals(df)
    df = compute_age_categories(df)
    df = drop_unused_columns(df)
    df = reorder_columns(df)

    return df


# =========================
# Entry point
# =========================

if __name__ == "__main__":
    all_data = pd.concat(
        [transform_lic_file(year) for year in YEARS],
        ignore_index=True
    )

    all_data.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Fichier final généré : {OUTPUT_FILE}")