import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np






def LinReg(df_filtered, year):

    df_filtered = df_filtered.sort_values("year")

   # df_filtered.loc[df_filtered['year'] == 2021, 'total_lic'] = None
    df_filtered=df_filtered.groupby('year',as_index=False).agg(
        total_lic=('total_lic','sum')
        )
    df_filtered=df_filtered[["year","total_lic"]]
    
    df_filtered['total_lic'] = df_filtered['total_lic'].interpolate()
    
    X=df_filtered[["year"] ] 
    y=df_filtered[["total_lic"]]
    split_index = int(len(df_filtered) * 0.6)

    X_train = X.iloc[:split_index]
    X_test  = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test  = y.iloc[split_index:]
    regressor=LinearRegression()
    regressor.fit(X_train, y_train)

    regressor.fit(X, y)


    last_year=df_filtered["year"].max()
    
    if year > last_year :
        future_years = pd.DataFrame({
            "year": range(last_year +1, year+1)})

        future_pred = regressor.predict(future_years)
        fp=pd.Series(np.concatenate(future_pred),copy=False)
        
        df_future_pred = pd.DataFrame({
        "year": future_years["year"],
        "total_lic": fp
         })
        print('#########################################################')
        print(df_future_pred["year"].unique())
        print('#########################################################')
        df_future_pred=pd.concat([df_filtered,df_future_pred])
        df_future_pred=df_future_pred.groupby("year",as_index=False).agg(
            total_lic=('total_lic','sum')
            )
        print(df_future_pred)
    else:
        df_future_pred = df_filtered


    return df_future_pred

