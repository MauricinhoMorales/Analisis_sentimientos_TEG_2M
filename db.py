import sys
from pandas.core.frame import DataFrame
import psycopg2
import psycopg2.extras as extras
import pandas as pd

#connect to the db
param_dic = {
    "host":"localhost",
    "database":"TEG2Mv0.1",
    "user":"postgres",
    "password":"26444352m",
    "port":5432
}

#Import .csv file
df = pd.read_csv('Tweets_Clasificados3.csv')
df = df.rename(columns={
    "date": "tweet_date", 
    "username": "tweet_username",
    "tweet": "tweet",
    "tweet_translated": "tweet_translate",
    "sentimiento": "tweet_sentiment",
    "opinion": "tweet_opinion"
})

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    connection = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return connection

def execute_values(connection, dataframe, table):
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in dataframe.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(dataframe.columns))
    # SQL quert to execute
    query  = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = connection.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()
        return 1
    print("execute_values() done")
    cursor.close()
    return None

conn = connect(param_dic)
execute_values(connection=conn,dataframe=df,table='tweets')
