"""."""
import flask
from flask import jsonify, request

from tweets_management import tweets_management
from tweets_ngrams import tweets_ngrams
from tweets_classification import tweets_classification
from fill_db import fill_table_tweets_model_opinion,\
        fill_table_tweets_model_sentiment,fill_table_tweets_model_test,\
        db_table_to_dataframe
from connection_db import TweetsModel, TweetsModelOpinion, \
    TweetsModelSentimient, TweetsTestModel, StadisticsModel, app, db
from general_functions import get_sentiment_general_probability_distribution,\
        get_opinion_general_probability_distribution,get_probability_by_date,\
        get_monograms_list,get_ngrams_list,get_general_probability_distribution

SQLALCHEMY_TRACK_MODIFICATIONS = False

# ! Variables para identificar a que carpetas seran guardadas
BATCH_FOLDER = 'batch'
SENTIMIENTO_FOLDER = 'sentimiento'
OPINION_FOLDER = 'opinion'
MENSAJES_FOLDER = 'mensajes'

@app.route('/api', methods=['GET','POST'])
def test_route():
    """."""
    if flask.request.method == 'POST':
        return {
            'status' : 'Ok',
            'method':'POST'
        }
    elif flask.request.method == 'GET':
        return {
            'status' : 'Ok',
            'method':'GET'
        }
    return None

@app.route('/api/dataframe', methods=['GET'])
def test_db_to_dataframe():
    """."""
    if flask.request.method == 'GET':
        db_table_to_dataframe(table='tweets_model_sentiment')
        return {
            'status' : 'Ok',
            'method':'PosgresSQL table to a DataFrame'
        }
    return None

@app.route('/tweets/fill', methods=['GET'])
def fill_db_route():
    """."""
    fill_table_tweets_model_test()
    fill_table_tweets_model_opinion()
    fill_table_tweets_model_sentiment()
    return {
        'status':'OK'
    }

@app.route('/tweets', methods=['GET','POST'])
def tweets_route():
    """."""
    if not request.args:
        return {
            'status': 'error',
            'message': "parameter not provided, Please \
            specify an folder adding at the end of the \
            url '?parameter=***' "
        }
    elif request.args['parameter'] == 'sentimiento':
        if flask.request.method == 'GET':
            all_tweets = TweetsModelSentimient.query.all()
            output = []
            for tweet in all_tweets:
                curr_tweet = {}
                curr_tweet['tweet_id'] = tweet.tweet_id
                curr_tweet['tweet'] = tweet.tweet
                curr_tweet['tweet_tokenized'] = tweet.tweet_tokenized
                curr_tweet['tweet_translated'] = tweet.tweet_translated
                curr_tweet['tweet_translated_tokenized'] = tweet.tweet_translated_tokenized
                curr_tweet['tweet_sentiment'] = tweet.tweet_sentiment
                output.append(curr_tweet)
            return jsonify(output)
    elif request.args['parameter'] == 'opinion':
        if flask.request.method == 'GET':
            all_tweets = TweetsModelOpinion.query.all()
            output = []
            for tweet in all_tweets:
                curr_tweet = {}
                curr_tweet['tweet_id'] = tweet.tweet_id
                curr_tweet['tweet'] = tweet.tweet
                curr_tweet['tweet_tokenized'] = tweet.tweet_tokenized
                curr_tweet['tweet_translated'] = tweet.tweet_translated
                curr_tweet['tweet_translated_tokenized'] = tweet.tweet_translated_tokenized
                curr_tweet['tweet_opinion'] = tweet.tweet_opinion
                output.append(curr_tweet)
            return jsonify(output)
    elif request.args['parameter'] == 'test':
        if flask.request.method == 'GET':
            all_tweets = TweetsTestModel.query.all()
            output = []
            for tweet in all_tweets:
                curr_tweet = {}
                curr_tweet['tweet_id'] = tweet.tweet_id
                curr_tweet['tweet'] = tweet.tweet
                curr_tweet['tweet_tokenized'] = tweet.tweet_tokenized
                curr_tweet['tweet_translated'] = tweet.tweet_translated
                curr_tweet['tweet_translated_tokenized'] = tweet.tweet_translated_tokenized
                curr_tweet['tweet_sentiment'] = tweet.tweet_sentiment
                curr_tweet['tweet_opinion'] = tweet.tweet_opinion
                output.append(curr_tweet)
            return jsonify(output)
        elif flask.request.method == 'POST':
            tweet_data = request.get_json()
            print(tweet_data)
            tweet_new = TweetsTestModel(
                tweet_id = tweet_data['tweet_id'],
                tweet_date = tweet_data['tweet_date'],
                tweet_username = tweet_data['tweet_username'],
                tweet = tweet_data['tweet'],
                tweet_translated = tweet_data['tweet_translated'],
                tweet_sentiment = tweet_data['tweet_sentiment'],
                tweet_opinion = tweet_data['tweet_opinion'],
                tweet_translated_tokenized = [''],
                tweet_tokenized = ['']
            )
            db.session.add(tweet_new)
            db.session.commit()
            return jsonify(tweet_data)
    else:
        return {
            'status': 'error',
            'message': "Error: Not a valid folder field provided. Please\
            specify an folder adding at the end of the\
            url '?parameter=***'."
        }
    return None

@app.route('/tweets/scrapping',methods=['GET'])
def scrap_tweets():
    """."""
    tweets_management.scraping(1000,BATCH_FOLDER)

@app.route('/tweets/cleaning',methods=['GET'])
def clean_tweets():
    """."""
    if request.args['parameter'] == 'sentiment':
        sentimiento = tweets_management(SENTIMIENTO_FOLDER)
        sentimiento.cleaning()
    elif request.args['parameter'] == 'opinion':
        opinion = tweets_management(OPINION_FOLDER)
        opinion.cleaning()

@app.route('/tweets/classification',methods=['GET'])
def classify_tweets():
    """."""
    df_from_db_test = db_table_to_dataframe(table='tweets_test')

    if request.args['parameter'] == 'sentimiento':
        df_from_db = db_table_to_dataframe(table='tweets_model_sentiment')

        sorter_sentimiento = tweets_classification(SENTIMIENTO_FOLDER,df_from_db)
        sorter_sentimiento.training(0.1,0.9)
        sorter_sentimiento.test_Naive_Bayes()
        sorter_sentimiento.test_SVM()
        sorter_sentimiento.test_Decision_Tree()
        sorter_sentimiento.test_Max_Entropy()
        result_df = sorter_sentimiento.test_batch(df_to_test=df_from_db_test,category='sentimiento')
        fill_table_tweets_model_test(dataframe_to_fill=result_df)

    elif request.args['parameter'] == 'opinion':
        df_from_db = db_table_to_dataframe(table='tweets_model_opinion')

        sorter_opinion = tweets_classification(OPINION_FOLDER,df_from_db)
        sorter_opinion.training(0.1,0.9)
        sorter_opinion.test_Naive_Bayes()
        sorter_opinion.test_SVM()
        sorter_opinion.test_Decision_Tree()
        sorter_opinion.test_Max_Entropy()
        result_df = sorter_opinion.test_batch(df_to_test=df_from_db_test,category='opinion')
        fill_table_tweets_model_test(dataframe_to_fill=result_df)

    else:
        return "Error: Not a valid folder field provided. Please \
            specify an folder adding at the end of the \
            url '?parameter=***'."

    return {
        "message":"Clasificación Completada"
    }

@app.route('/tweets/ngrams',methods=['GET'])
def get_ngrams_tweets():
    """."""
    if request.args['parameter'] == 'sentiment':
        n_grams_sentimiento = tweets_ngrams(SENTIMIENTO_FOLDER)
        n_grams_sentimiento.monogramming()
        n_grams_sentimiento.ngraming()
    elif request.args['parameter'] == 'opinion':
        n_grams_opinion = tweets_ngrams(OPINION_FOLDER)
        n_grams_opinion.monogramming()
        n_grams_opinion.ngraming()
    else:
        return "Error: Not a valid folder field provided. Please \
            specify an folder adding at the end of the \
            url '?parameter=***'."
    return None

@app.route('/stadistics/general_probability_distribution', methods=['GET'])
def g_probability_d():
    """."""
    if not request.args:
        return {
            'status': 'error',
            'message': "parameter not provided, Please \
            specify an folder adding at the end of the \
            url '?parameter=***' "
        }
    elif request.args['parameter'] == 'sentimiento':
        df_from_db = db_table_to_dataframe(table='tweets_model_sentiment')
        return get_sentiment_general_probability_distribution(df=df_from_db)
    elif request.args['parameter'] == 'opinion':
        df_from_db = db_table_to_dataframe(table='tweets_model_opinion')
        return get_opinion_general_probability_distribution(df=df_from_db)
    elif request.args['parameter'] == 'test':
        df_from_db = db_table_to_dataframe(table='tweets_test')
        return get_general_probability_distribution(df=df_from_db)
    else:
        return "Error: Not a valid folder field provided. Please \
            specify an folder adding at the end of the \
            url '?parameter=***'."

@app.route('/stadistics/distribution_by_date', methods=['GET'])
def distribution_by_date():
    """."""
    df_from_db = db_table_to_dataframe(table='tweets_test')
    return get_probability_by_date(df=df_from_db)

@app.route('/stadistics/distribution_monograms', methods=['GET'])
def distribution_by_monograms():
    """."""
    if not request.args:
        return {
            'status': 'error',
            'message': "parameter not provided, Please \
            specify an folder adding at the end of the \
            url '?parameter=***' "
        }
    elif request.args['parameter'] == 'sentimiento':
        df_from_db = db_table_to_dataframe(table='tweets_model_sentiment')
    elif request.args['parameter'] == 'opinion':
        df_from_db = db_table_to_dataframe(table='tweets_model_opinion')
    elif request.args['parameter'] == 'test':
        df_from_db = db_table_to_dataframe(table='tweets_test')
    else:
        return {
            'status': 'error',
            'message': "Error: Not a valid folder field provided. Please\
            specify an folder adding at the end of the\
            url '?parameter=***'."
        }
    return get_monograms_list(df=df_from_db)

@app.route('/stadistics/distribution_ngrams', methods=['GET'])
def distribution_by_ngrams():
    """."""
    ngram = 2
    if not request.args:
        return {
            'status': 'error',
            'message': "parameter not provided, Please \
            specify an folder adding at the end of the \
            url '?parameter=***' "
        }
    if request.args['ngram'] == '2':
        ngram = 2
    elif request.args['ngram'] == '3':
        ngram = 3
    else:
        return {
            'status': 'error',
            'message': "Error: Not a valid folder field provided. Please\
            specify an folder adding at the end of the\
            url '&ngram=*'."
        }
    if request.args['parameter'] == 'sentimiento':
        df_from_db = db_table_to_dataframe(table='tweets_model_sentiment')
    elif request.args['parameter'] == 'opinion':
        df_from_db = db_table_to_dataframe(table='tweets_model_opinion')
    elif request.args['parameter'] == 'test':
        df_from_db = db_table_to_dataframe(table='tweets_test')
    else:
        return {
            'status': 'error',
            'message': "Error: Not a valid folder field provided. Please\
            specify an folder adding at the end of the\
            url '?parameter=***'."
        }
    return get_ngrams_list(df=df_from_db,ngram_value=ngram)

if __name__ == '__main__':
    app.run()
