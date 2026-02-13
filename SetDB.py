import DBConnector as dbc
import pandas as pd
import re
########################
# DO NOT RUN IT
# EXAMPLE ONLY
#
########################

datamedia = pd.read_csv("data_media.csv")
datalicenses=pd.read_csv("data_licenses.csv")
datamedia["évènement"]=datamedia["évènement"].astype('str')
datamedia["sport"]=datamedia["sport"].astype('str')
datamedia["année"]=datamedia["année"].astype('float64')
datamedia["audience TV moynne total event"]=datamedia["audience TV moynne total event"].astype('float64')
datamedia["audience TV moy par match"]=datamedia["audience TV moy par match"].astype('float64')
datamedia["Nombre de matchs"]=datamedia["Nombre de matchs"].astype('float64')
datamedia["heures d'antenne (télévision linéaire)"]=datamedia["heures d'antenne (télévision linéaire)"].astype('float64')
datamedia["nombre de posts RS"]=datamedia["nombre de posts RS"].astype('float64')
datamedia=datamedia.rename(columns={"évènement": "sport_event", "année": "year","audience TV moynne total event": "avrg_tv_aud","audience TV moy par match": "avrg_tv_match", "Nombre de matchs": "total_match", "heures d'antenne (télévision linéaire)": "hours_live","nombre de posts RS": "numb_of_post"  })
print(datalicenses.info())
datamedia = datamedia.replace({float('nan'): None})
datalicenses=datalicenses.drop(["code_commune","nom_commune","num_departement"],axis=1)
print(datalicenses.head(20))


datalicenses["total_lic"] = datalicenses["total_lic"].replace({".": ""}, regex=True)
datalicenses["total_f"] = datalicenses["total_f"].replace({".": ""}, regex=True)
datalicenses["total_h"] = datalicenses["total_h"].replace({".": ""}, regex=True)
datalicenses["total_lic"]=pd.to_numeric(datalicenses['total_lic'])
datalicenses["total_f"]=pd.to_numeric(datalicenses['total_f'])
datalicenses["total_h"]=pd.to_numeric(datalicenses['total_h'])
datalicenses = datalicenses.replace({"'": ""}, regex=True)
datalicenses = datalicenses.replace({'"': ""}, regex=True)
datalicenses = datalicenses.replace({'-': " "}, regex=True)
datalicenses = datalicenses.replace({',': ""}, regex=True)
result=datalicenses.groupby(["annee","region","nom_fed"], as_index=False).agg(
total_license=('total_lic','sum'),
total_f=('total_f','sum'),
total_h=('total_h','sum')
)
result.to_csv("licenses_by_year_region_fed.csv", index=False)
#conn=dbc.TryConnect()

#for i,row in datamedia.iterrows():
    #quer="INSERT INTO media_table.media_data (sport_event,sport,year,avrg_tv_aud,avrg_tv_match,total_match,hours_live,numb_of_post) " \
    #"VALUES ('"+row["sport_event"]+"','"+row["sport"]+"','"+str(row["year"])+"','"+str(row["avrg_tv_aud"])+"','"+str(row["avrg_tv_match"])+"',"
    #"'"+str(row["total_match"])+"','"+str(row["hours_live"])+"','"+str(row["numb_of_post"])+"')"    
    #print(quer)
    #conn._execute_query(quer)
    #conn.commit()


# for i,row in datalicenses.iterrows():
#     quer="INSERT INTO media_table.licenses (year, code_commune, nom_commune, num_dep, region, code_fed, nom_fed, total_lic, total_f, total_h, h_1_9, h_10_19, h_20_29,h_30_59, " \
#     "h_60_74, h_75, f_1_9, f_10_19, f_20_29, f_30_59, f_60_74, f_75) " \
#     "VALUES ('"+str(row["annee"])+"','"+str(row["code_commune"])+"','"+str(row["nom_commune"])+"','"+str(row["num_departement"])+"','"+str(row["region"])+"','"+str(row["code_fed"])+"','"+str(row["nom_fed"])+"','"+str(row["total_lic"])+"','"+str(row["total_f"])+"','"+str(row["total_h"])+"','"+str(row["h_1_9"])+"','"+str(row["h_10_19"])+"','"+str(row["h_20_29"])+"','"+str(row["h_30_59"])+"','"+str(row["h_60_74"])+"','"+str(row["h_75"])+"','"+str(row["f_1_9"])+"','"+str(row["f_10_19"])+"','"+str(row["f_20_29"])+"','"+str(row["f_30_59"])+"','"+str(row["f_60_74"])+"','"+str(row["f_75"])+"')"   
#     print(quer)
#     conn._execute_query(quer)
#     conn.commit()
  

#dbc.CloseCon(conn)
