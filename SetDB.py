import DBConnector as dbc
import pandas as pd
import re
########################
# DO NOT RUN IT
# EXAMPLE ONLY
#
########################

datamedia = pd.read_csv("data_media.csv")
datamedia["évènement"]=datamedia["évènement"].astype('str')
datamedia["sport"]=datamedia["sport"].astype('str')
datamedia["année"]=datamedia["année"].astype('float64')
datamedia["audience TV moynne total event"]=datamedia["audience TV moynne total event"].astype('float64')
datamedia["audience TV moy par match"]=datamedia["audience TV moy par match"].astype('float64')
datamedia["Nombre de matchs"]=datamedia["Nombre de matchs"].astype('float64')
datamedia["heures d'antenne (télévision linéaire)"]=datamedia["heures d'antenne (télévision linéaire)"].astype('float64')
datamedia["nombre de posts RS"]=datamedia["nombre de posts RS"].astype('float64')
datamedia=datamedia.rename(columns={"évènement": "sport_event", "année": "year","audience TV moynne total event": "avrg_tv_aud","audience TV moy par match": "avrg_tv_match", "Nombre de matchs": "total_match", "heures d'antenne (télévision linéaire)": "hours_live","nombre de posts RS": "numb_of_post"  })
print(datamedia.info())
datamedia = datamedia.replace({float('nan'): None})
conn=dbc.TryConnect()

for i,row in datamedia.iterrows():
    quer="INSERT INTO media_table.media_data (sport_event,sport,year,avrg_tv_aud,avrg_tv_match,total_match,hours_live,numb_of_post) VALUES ('"+row["sport_event"]+"','"+row["sport"]+"','"+str(row["year"])+"','"+str(row["avrg_tv_aud"])+"','"+str(row["avrg_tv_match"])+"','"+str(row["total_match"])+"','"+str(row["hours_live"])+"','"+str(row["numb_of_post"])+"')"    
    print(quer)
    conn._execute_query(quer)
    conn.commit()

print(conn._execute_query("SELECT * FROM media_table.media_data"))
dbc.CloseCon(conn)
