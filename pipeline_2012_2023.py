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

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# FULL PERIOD
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

def clean_columns(df):
    '''Premier cleaning des colonnes sur l'ensemble des années'''
    
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

def clean_numeric_columns_2014(df):
    '''Transforme les colonnes numérique en int, pour éviter les bug d'analyse '''
    
    cols = df.columns[3:65]

    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    
    return df

def add_year(df, year: int):
    ''' Ajout de l'année en colonne pour chacune des années'''
    
    df["annee"] = year
    return df

def clean_federation_name(text):
    ''' Mise en forme de la colonne "nom_fed" et suppression des termes FEDERATION FRANCAISE, pour n'avoir que les noms des sports'''
    
    if pd.isna(text):
        return text
    
    # 1.mettre en majuscules
    text = text.upper()
    
    # 2. enlever accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    # 3. supprimer FF, DE, D'
    text = re.sub(r"\bFF\b", "", text)
    text = re.sub(r"\bDE\b", "", text)
    text = re.sub(r"\bD['’]", "", text)  # gère ' et ’
    text = re.sub(r"\bDES\b", "", text)
    text = re.sub(r"\bDU\b", "", text)
    text = re.sub(r"\bF\b", "", text)
    text = re.sub(r"\bFEDERATION FRANCAISE\b", "", text)

    
    # 4. enlever espaces multiples
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def clean_federation(df):
    ''' Mise en application de la fonction clean_federation_name'''

    if "nom_fed" in df.columns:
        df["nom_fed"] = df["nom_fed"].apply(clean_federation_name)
    return df

def normalize_name(text):
    ''' Agrégation des noms de fédérations similaires pour éviter les doublons'''
    
    if pd.isna(text):
        return text

    # supprimer mots parasites fréquents
    stopwords = [
        "FEDERATION", "DISCIPLINES ASSOCIEES", "DISCIPLINES ASSOCIEES",
        "ET DA", "ET DISCIPLINES ASSOCIEES"
    ]
    
    for word in stopwords:
        text = text.replace(word, "")

    return text

mapping = {
    "AIKIDO AIKIBUDO ET AFFINITAIRES": "AIKIDO ET BUDO",
    "AIKIDO AIKIBUDO ET AINITAIRES": "AIKIDO ET BUDO",
    "AIKIDO ET BUDO": "AIKIDO ET BUDO",
    "AIKIDO AIKIBUDO ET A FRANCAISEINITAIRES":"AIKIDO ET BUDO",
    "AIKIDO, AIKIBUDO ET AFFINITAIRES":"AIKIDO ET BUDO",
    "BALL TRAP": "BALL TRAP ET TIR A BALLE",
    "BASEBALL SOFTBALL":"BASEBALL ET SOFTBALL",
    "BOWLING ET SPORT QUILLES":"BOWLING ET SPORTS QUILLES",
    "BOXE FRANCAISE SAVATE ET":"BOXE FRANCAISE SAVATE",
    "CANOE KAYAK ET SPORTS PAGAIE":"CANOE KAYAK",
    "DES ARTS ENERGETIQUES ET MARTIAUX CHINOIS":"ARTS ENERGETIQUES ET MARTIAUX CHINOIS",
    "FLYING DISC FRANCE":"FLYING DISC",
    "HOCKEY SUR GLACE":"HOCKEY",
    "D\x92HALTEROPHILIE MUSCULATION":'HALTEROPHILIE MUSCULATION',
    "JOUTES ET SAUVETAGE NAUTIQUE":'JOUTE ET SAUVETAGE NAUTIQUE',
    "JUDO JUJITSU ET":"JUDO JUJITSU",
    "JUDO JUJITSU KENDO":"JUDO JUJITSU",
    "JUDO JUJITSU KENDO ET":"JUDO JUJITSU",
    "KARATE ET":"KARATE",
    "KARATE ET DISCIPLINES ASSOCIES":"KARATE",
    "KICK BOXING MUAY THAI ET":"KICK BOXING MUAY THAI",
    'LA COURSE CAMARGUAISE':'COURSE CAMARGUAISE',
    "LA COURSE LANDAISE":"COURSE LANDAISE",
    "LA COURSE ORIENTATION":"COURSE ORIENTATION",
    "LA MONTAGNE ET ESCALADE":"MONTAGNE ET ESCALADE",
    "LA MONTAGNE ET LESCALADE":"MONTAGNE ET ESCALADE",
    "LA RANDONNEE PEDESTRE":"RANDONNEE PEDESTRE",
    "LA RETRAITE SPORTIVE":"RETRAITE SPORTIVE",
    "LUTTE ET":"LUTTE",
    "NATIONALE AERONAUTIQUE":"AERONAUTIQUE",
    "NATIONALE SPORT EN MILIEU RURAL":"SPORT EN MILIEU RURAL",
    "NAUTIQUE PECHE SPORTIVE EN APNEE":"PECHE SPORTIVE EN APNEE",
    "OMNISPORTS PERSONNELS LEDUCATION NATIONALE":"OMNISPORTS PERSONNELS EDUCATION NATIONALE JEUNESSE ET SPORTS",
    "OMNISPORTS PERSONNELS LEDUCATION NATIONALE LA JEUNESSE ET SPORTS":"OMNISPORTS PERSONNELS EDUCATION NATIONALE JEUNESSE ET SPORTS",
    "OMNSISPORTS PERSONNELS LEDUCATION NATIONALE ET JEUNESSE ET SPORTS":"OMNISPORTS PERSONNELS EDUCATION NATIONALE JEUNESSE ET SPORTS",
    "PLANEUR ULTRA LEGER MOTORISE":"PLANEUR ULTRALEGER MOTORISE",
    "ROLLER SPORTS":"ROLLER ET SKATEBOARD",
    "SAVATE BOXE FRANCAISE":"BOXE FRANCAISE SAVATE",
    "SAVATE BOXE FRANCAISE ET":"BOXE FRANCAISE SAVATE",
    "SKI NAUTIQUE ET WAKE BOARD":"SKI NAUTIQUE ET WAKEBOARD",  
    "SPORTIVE ASPTT":"ASPTT",
    "SPORTIVE LA POLICE NATIONALE":"FEDERATION SPORTIVE LA POLICE NATIONALE",
    "SPORTIVE TWIRLING BATON":"TWIRLING BATON",
    "SPORTS BILLARD":"BILLARD",
    "SPORTS TRAINEAU SKI PULKA ET CROSS CANINS":"PULKA ET TRAINEAU A CHIENS",
    "SPORTS TRAINEAU":"PULKA ET TRAINEAU A CHIENS",
    "SPORTS TRAINEAU SKI VTT JOERING ET CANICROSS":"TRAINEAU SKI VTT JOERING ET CANICROSS",
    "TAEKWONDO ET":"TAEKWONDO",
    "TRIATHLON":"TRIATHLON ET DISCIPLINES ENCHAINEES",
    "UNION FRANCAISE \x9cUVRES LAIQUES EDUCATION PHYSIQUE":"UNION FRANCAISE OEUVRES LAIQUES EDUCATION PHYSIQUE",
    "UNION FRANCAISE ŒUVRES LAIQUES EDUCATION PHYSIQUE":"UNION FRANCAISE OEUVRES LAIQUES EDUCATION PHYSIQUE",
    "VOLLEY":"VOLLEYBALL",
    "VOLLEY BALL":"VOLLEYBALL"
}

def apply_normalize_name(df):
    df["nom_fed"] = df["nom_fed"].apply(normalize_name).replace(mapping)

    return df

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# 2012 -> 2018
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

def import_dept_num(df):
    '''Import du numéro de département en fusionnant une base externe '''

    communes_dept = pd.read_csv("data/recap_communes_par_departement.csv")
    communes_dept = communes_dept.rename(columns={"Département":"num_departement","Code Commune":"code_commune"})
    df = df.merge(communes_dept,how="inner",on="code_commune")

    return df

def rename_columns_2012_2018(df):
    ''' Normalisation du nom des colonnes'''

    synonyms = {
        "nom_commune": ["libelle", "libgeo"],
        "code_fed": ["fed"],
        "code_commune": ["newcog2", "cog2"],
        "nom_fed": ["federation"],
#       "total_lic": ["l"],
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

def compute_age_categories_2012_2018(df):
    ''' Calcul des nouvelles catégories d'âges'''

    age_mapping = {
        "1_9": ["0_4", "5_9"],
        "10_19": ["10_14", "15_19"],
        "20_29": ["20_29"],
        "30_59": ["30_44", "45_59"],
        "60_74": ["60_74"],
        "75": ["75", "75_99"]  
    }
    

    for sex in ["f", "h"]:
        for new_cat, source_cats in age_mapping.items():
            cols = [f"l_{age}_{sex}" for age in source_cats if f"l_{age}_{sex}" in df.columns]
            if cols:  # s'assure qu'il y a au moins une colonne
                df[f"{sex}_{new_cat}"] = df[cols].sum(axis=1)
            else:
                df[f"{sex}_{new_cat}"] = 0  # si aucune colonne, mettre 0
    return df

def compute_totals_2012_2023(df):
    ''' calcul des totaux de licences par sexe'''

    df["total_lic"] = df["total_f"] + df["total_h"]

    return df

def import_region(df):
    ''' Import d'une base externe pour connaitre les codes et noms des régions'''

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
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# 2019 -> 2023
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


def rename_columns_2019_2023(df):
    ''' Normalisation noms des colonnes'''

    rename_map = {"code commune":"code_commune",
                  "commune":"nom_commune",
                  "departement":"num_departement",
                  "code":"code_fed",
                  "federation":"nom_fed",
                  "total":"total_lic"}
    return df.rename(columns=rename_map)

def format_departement(df):
    ''' Mettre les colonnes de numéros de département en texte'''

    df["num_departement"] = df["num_departement"].astype(str).str.zfill(2)
    return df

def compute_totals_2019_2023(df):
    ''' calcul des totaux de licences par sexe'''

    f_cols = [col for col in df.columns if col.startswith("f_")]
    h_cols = [col for col in df.columns if col.startswith("h_")]

    df["total_f"] = df[f_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    df["total_h"] = df[h_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    df["total_lic"] = df["total_f"] + df["total_h"]

    return df

def compute_age_categories_2019_2023(df):
    ''' calcul des licenciés par catégorie d'âge'''

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

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# PIPELINE OF ACTIONS
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

def reorder_columns(df):
    ''' Ordonnancement des colonnes pour le dataset final'''

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
    ''' Pipeline final des différentes fonctions'''
    
    print(f"Processing year {year}...")

    # Les années antérieures à 2015 ont des encodages différents :
    file_path = f"{DATA_PATH}/lic-data-{year}.csv"
    if year <= 2015:
        df = pd.read_csv(file_path, low_memory=False, encoding="utf-8-sig")
    elif year >= 2019:
        df = pd.read_csv(file_path, sep=";", low_memory=False, encoding="utf-8")
    else:
        df = pd.read_csv(file_path, sep=";", encoding="latin1", low_memory=False)

    if year == 2014:
        df = clean_numeric_columns_2014(df)
    df = clean_columns(df)
    df = add_year(df, year)

    # Renommage des colonnes et calculs:
    if year <= 2018:
        df = rename_columns_2012_2018(df)
        df = import_dept_num(df)
        df = compute_age_categories_2012_2018(df)
        df = compute_totals_2012_2023(df)
    else:
        df = rename_columns_2019_2023(df)
        df = format_departement(df)
        df = compute_totals_2019_2023(df)
        df = compute_age_categories_2019_2023(df)
          
    # Les années antérieures à 2014 n'ont pas de région
    if year <= 2014:
        df = import_region(df)

    df = clean_federation(df)
    df = apply_normalize_name(df)    
    df = reorder_columns(df)

    return df

if __name__ == "__main__":
    # Dataset complet par communes :
    all_data = pd.concat(
        [transform_lic_file(year) for year in YEARS],
        ignore_index=True
    )

    all_data.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Fichier final généré : {OUTPUT_FILE}")

    # Dataset agrégé par région / année / fédération
    cols_to_sum=[
    "total_f",
    "total_h",
    'h_1_9',
    'h_10_19',
    'h_20_29',
    'h_30_59',
    'h_60_74',
    'h_75',
    'f_1_9',
    'f_10_19',
    'f_20_29',
    'f_30_59',
    'f_60_74',
    'f_75']
    
    # Forcer les colonnes numériques en int
    all_data[cols_to_sum] = all_data[cols_to_sum].apply(pd.to_numeric, errors="coerce").astype("Int64")
    # Agréger en région, avec somme des colonnes numériques (licences)
    df_region = all_data.groupby(["region",'annee',"nom_fed"])[cols_to_sum].sum().reset_index()
    # Création de la colonne "total_license" car elle avait été nommé différement dès la création du fichier régional
    df_region["total_license"] = df_region["total_h"] + df_region["total_f"]
    
    region_output = "data/licenses_by_year_region_fed.csv"
    df_region.to_csv(region_output, index=False)

    print(f"✅ Fichier région agrégé généré : {region_output}")
