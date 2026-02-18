# JedhaProject
A repo for the final project of DAFS in jehda bootcamp


# DBConnector.py
The script DBConnector contains three functions and four starting variables. The goal of the script is to allow the user to connect to the AWS database and get the env variables necessary to access the database.

## Variable
### conn
variable is set as None to avoid any conflict with cached data. the variable will be used as the connection to the database
## #queryLicenses
The query to get the dataset for licenses per region, the query is stored in the .env (not available in the git)
### queryMedias
The query to get the dataset for medias and averages views for big sport events starting 2012, the query is stored in the .env (not available in the git)
### queryClubs
The query to get the dataset for clubs licenses starting 1949 to 2023, the query is stored in the .env (not available in the git)