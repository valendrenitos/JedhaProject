import pandas as pd
from sklearn.linear_model import LinearRegression







def LinReg(df_filtered, year):
    df_filtered = df_filtered.sort_values("year")

    df_filtered.loc[df_filtered['year'] == 2021, 'total_lic'] = None
    df_filtered['total_lic'] = df_filtered['total_lic'].interpolate(method='linear')
    
    X=df_filtered["year"]  
    y=df_filtered["total_lic"]
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
            "annee": range(last_year +1, year)})

        future_pred = regressor.predict(future_years)

        df_future_pred = pd.DataFrame({
        "annee": future_years["annee"],
        "total_pred": future_pred
         })
    
    else:
        df_future_pred = df_filtered


    return(df_future_pred)

