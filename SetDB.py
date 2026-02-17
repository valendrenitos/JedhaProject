import DBConnector as dbc
import pandas as pd
import re
########################
# DO NOT RUN IT
# EXAMPLE ONLY
#
########################
data_clubs = pd.read_csv("lic_clean_49_24.csv")
data_clubs = data_clubs.drop(["indexation"],axis=1)
data_clubs=data_clubs.astype("float64")

data_clubs2 = pd.read_csv("lic_clean_49_24.csv")
data_clubs2 = data_clubs.drop(["indexation"],axis=1)
data_clubs2=data_clubs.astype("float64")
#datamedia = pd.read_csv("data_media.csv")
# datalicenses=pd.read_csv("data_licenses.csv")
# datamedia["évènement"]=datamedia["évènement"].astype('str')
# datamedia["sport"]=datamedia["sport"].astype('str')
# datamedia["année"]=datamedia["année"].astype('float64')
# datamedia["audience TV moynne total event"]=datamedia["audience TV moynne total event"].astype('float64')
# datamedia["audience TV moy par match"]=datamedia["audience TV moy par match"].astype('float64')
# datamedia["Nombre de matchs"]=datamedia["Nombre de matchs"].astype('float64')
# datamedia["heures d'antenne (télévision linéaire)"]=datamedia["heures d'antenne (télévision linéaire)"].astype('float64')
# datamedia["nombre de posts RS"]=datamedia["nombre de posts RS"].astype('float64')
#datamedia=datamedia.rename(columns={"évènement": "sport_event", "année": "year","audience TV moynne total event": "avrg_tv_aud","audience TV moy par match": "avrg_tv_match", "Nombre de matchs": "total_match", "heures d'antenne (télévision linéaire)": "hours_live","nombre de posts RS": "numb_of_post"  })

#datamedia = datamedia.replace({float('nan'): None})
# datalicenses=datalicenses.drop(["code_commune","nom_commune","num_departement"],axis=1)

# datalicenses = datalicenses.replace({"'": ""}, regex=True)
# datalicenses = datalicenses.replace({'"': ""}, regex=True)
# datalicenses = datalicenses.replace({',': ""}, regex=True)
# cols = ["total_lic","total_f", "total_h", "h_1_9", "h_10_19", "h_20_29", "h_30_59",
#         "h_60_74", "h_75", "f_1_9", "f_10_19", "f_20_29", "f_30_59",
#         "f_60_74", "f_75"]
# datalicenses[cols] = datalicenses[cols].replace(r'\.', '', regex=True).replace('','0',regex=True).astype('float64')

# datalicenses.info()
# result=datalicenses.groupby(["annee","region","nom_fed"], as_index=False).agg(
# total_license=('total_lic','sum'),
# total_f=('total_f','sum'),
# total_h=('total_h','sum'),
# h_1_9=('h_1_9','sum'),
# h_10_19=('h_10_19','sum'),
# h_20_29=('h_20_29','sum'),
# h_30_59=('h_30_59','sum'),
# h_60_74=('h_60_74','sum'),
# h_75=('h_75','sum'),
# f_1_9=('f_1_9','sum'),
# f_10_19=('f_10_19','sum'),
# f_20_29=('f_20_29','sum'),
# f_30_59=('f_30_59','sum'),
# f_60_74=('f_60_74','sum'),
# f_75=('f_75','sum')
# )
# result.to_csv("licenses_by_year_region_fed.csv", index=False)
conn=dbc.TryConnect()

#for i,row in datamedia.iterrows():
    #quer="INSERT INTO media_table.media_data (sport_event,sport,year,avrg_tv_aud,avrg_tv_match,total_match,hours_live,numb_of_post) " \
    #"VALUES ('"+row["sport_event"]+"','"+row["sport"]+"','"+str(row["year"])+"','"+str(row["avrg_tv_aud"])+"','"+str(row["avrg_tv_match"])+"',"
    #"'"+str(row["total_match"])+"','"+str(row["hours_live"])+"','"+str(row["numb_of_post"])+"')"    
    #print(quer)
    #conn._execute_query(quer)
    #conn.commit()

# for i,row in result.iterrows():
#     quer="INSERT INTO media_table.licenses (year,  region,  nom_fed, total_lic, total_f, total_h, h_1_9, h_10_19, h_20_29,h_30_59,h_60_74, h_75, f_1_9, f_10_19, f_20_29, f_30_59, f_60_74, f_75) VALUES ('"+str(row["annee"])+"','"+str(row["region"])+"','"+str(row["nom_fed"])+"','"+str(row["total_license"])+"','"+str(row["total_f"])+"','"+str(row["total_h"])+"','"+str(row["h_1_9"])+"','"+str(row["h_10_19"])+"','"+str(row["h_20_29"])+"','"+str(row["h_30_59"])+"','"+str(row["h_60_74"])+"','"+str(row["h_75"])+"','"+str(row["f_1_9"])+"','"+str(row["f_10_19"])+"','"+str(row["f_20_29"])+"','"+str(row["f_30_59"])+"','"+str(row["f_60_74"])+"','"+str(row["f_75"])+"')"   
#     print(quer)
#     conn._execute_query(quer)
#     conn.commit()

for i,row in data_clubs.iterrows():
    quer="INSERT INTO media_table.club_total (annee,  olympics,  non_olympics, affinitaire, scholair, total) VALUES ('"+str(row["annee"])+"','"+str(row["olympique"])+"','"+str(row["non-olympique"])+"','"+str(row["affinitaire"])+"','"+str(row["scolaire"])+"','"+str(row["total"])+"')" 
    print(quer)
    conn._execute_query(quer)
    conn.commit()
  

for i,row in data_clubs2.iterrows():
    quer="INSERT INTO media_table.club_total (annee,  olympics,  non_olympics, affinitaire, scholair, total) VALUES ('"+str(row["annee"])+"','"+str(row["olympique"])+"','"+str(row["non-olympique"])+"','"+str(row["affinitaire"])+"','"+str(row["scolaire"])+"','"+str(row["total"])+"')" 
    print(quer)
    conn._execute_query(quer)
    conn.commit()
  

dbc.CloseCon(conn)
