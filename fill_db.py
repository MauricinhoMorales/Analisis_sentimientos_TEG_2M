"""."""
from os import linesep
import sys
from pandas.core.frame import DataFrame
import psycopg2
import psycopg2.extras as extras
import pandas as pd

#connect to the db
PARAM_DIC = {
    "host":"localhost",
    "database":"TEG2Mv0.1",
    "user":"postgres",
    "password":"26444352m",
    "port":5432
}

#Import .csv files
DF_PROCESSED_TWEETS_TEST = pd.read_csv('batch/Processed_Tweets_Test_v2.csv')
DF_PROCESSED_TWEETS_TEST = DF_PROCESSED_TWEETS_TEST.rename(columns={
    "date": "tweet_date",
    "tweet": "tweet",
    "username":"tweet_username",
    "tweet_translated": "tweet_translated",
    "tweet_tokenized": "tweet_tokenized",
    "tweet_translated_tokenized": "tweet_translated_tokenized"
})

DF_PROCESSED_TWEETS_OPINION = pd.read_csv('batch/Processed_Tweets2.csv')
DF_PROCESSED_TWEETS_OPINION = DF_PROCESSED_TWEETS_OPINION.rename(columns={
    "tweet": "tweet",
    "tweet_tokenized": "tweet_tokenized",
    "tweet_translated": "tweet_translated",
    "tweet_translated_tokenized": "tweet_translated_tokenized",
    "opinion": "tweet_opinion"
})

DF_PROCESSED_TWEETS_SENTIMIENT = pd.read_csv('batch/Processed_Tweets.csv')
DF_PROCESSED_TWEETS_SENTIMIENT = DF_PROCESSED_TWEETS_SENTIMIENT.rename(columns={
    "tweet": "tweet",
    "tweet_tokenized": "tweet_tokenized",
    "tweet_translated": "tweet_translated",
    "tweet_translated_tokenized": "tweet_translated_tokenized",
    "sentimiento": "tweet_sentiment"
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

CONN = connect(PARAM_DIC)

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
    print(f"Tabla {table} llenada con exito")
    cursor.close()
    return None

def empty_table(connection, table):
    """."""
    cursor = connection.cursor()
    query = f"TRUNCATE {table}"
    try:
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()
        return 1
    print(f"Tabla {table} vaciada con exito")
    cursor.close()
    return None

def fill_table_tweets_model_sentiment():
    """."""
    empty_table(connection=CONN, table='tweets_model_sentiment')
    execute_values(connection=CONN,
            dataframe=DF_PROCESSED_TWEETS_SENTIMIENT,
            table='tweets_model_sentiment')
    return "Done"

def fill_table_tweets_model_opinion():
    """."""
    empty_table(connection=CONN, table='tweets_model_opinion')
    execute_values(connection=CONN,
            dataframe=DF_PROCESSED_TWEETS_OPINION,
            table='tweets_model_opinion')

def fill_table_tweets_model_test(dataframe_to_fill: DataFrame=None):
    """."""
    empty_table(connection=CONN, table='tweets_test')
    if dataframe_to_fill is None:
        execute_values(connection=CONN,
            dataframe=DF_PROCESSED_TWEETS_TEST,
            table='tweets_test')
    else:
        execute_values(connection=CONN,
            dataframe=dataframe_to_fill,
            table='tweets_test')

def db_table_to_dataframe(table):
    """."""
    return pd.read_sql(f"select * from {table}", CONN)
