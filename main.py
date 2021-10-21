"""."""
import flask
from flask import jsonify, request

from tweets_management import tweets_management
from tweets_ngrams import tweets_ngrams
from tweets_classification import tweets_classification
from tweets_db_model import TweetsModel,app,db

# ! Variables para identificar a que carpetas seran guardadas
INDIVIDUAL_FOLDER = 'users'
BATCH_FOLDER = 'batch'
USERS_LIST = []

@app.route('/api', methods=['GET','POST'])
def test_route():
    """."""
    if flask.request.method == 'POST':
        return {
            'method':'POST'
        }
    elif flask.request.method == 'GET':
        return {
            'method':'GET'
        }
    return None

@app.route('/tweets', methods=['GET','POST'])
def tweets_route():
    """."""
    if flask.request.method == 'GET':
        all_tweets = TweetsModel.query.all()
        output = []
        for tweet in all_tweets:
            curr_tweet = {}
            curr_tweet['tweet_id'] = tweet.tweet_id
            curr_tweet['tweet_date'] = tweet.tweet_date
            curr_tweet['tweet_username'] = tweet.tweet_username
            curr_tweet['tweet'] = tweet.tweet
            curr_tweet['tweet_translate'] = tweet.tweet_translate
            curr_tweet['tweet_sentiment'] = tweet.tweet_sentiment
            curr_tweet['tweet_opinion'] = tweet.tweet_opinion
            output.append(curr_tweet)
        return jsonify(output)

    elif flask.request.method == 'POST':
        tweet_data = request.get_json()
        tweet_new = TweetsModel(
            tweet_id = tweet_data['tweet_id'],
            tweet_date = tweet_data['tweet_date'],
            tweet_username = tweet_data['tweet_username'],
            tweet = tweet_data['tweet'],
            tweet_translate = tweet_data['tweet_translate'],
            tweet_sentiment = tweet_data['tweet_sentiment'],
            tweet_opinion = tweet_data['tweet_opinion']
        )
        db.session.add(tweet_new)
        db.session.commit()
        return jsonify(tweet_data)
    return None

@app.route('/tweets/scrapping',methods=['GET'])
def scrap_tweets():
    """."""
    for user in USERS_LIST:
        user_twitter = tweets_management(user,BATCH_FOLDER)
        user_twitter.scraping(50)
        user_twitter.cleaning()
    return None

@app.route('/tweets/classification',methods=['GET'])
def classify_tweets():
    """."""
    if request.args['folder'] == 'individual':
        for user in USERS_LIST:
            sorter = tweets_classification(user,INDIVIDUAL_FOLDER)
            sorter.training(0.25)
            sorter.test_Naive_Bayes()
            sorter.test_SVM()
            sorter.test_Decision_Forest()
            sorter.test_Max_Entropy()
    elif request.args['folder'] == 'batch':
        for user in USERS_LIST:
            sorter = tweets_classification(user,BATCH_FOLDER)
            sorter.training(0.25)
            sorter.test_Naive_Bayes()
            sorter.test_SVM()
            sorter.test_Decision_Forest()
            sorter.test_Max_Entropy()
    else:
        return "Error: Not a valid folder field provided. Please specify an folder adding at the end of the url '?folder=***'."

    return None

@app.route('/tweets/ngrams',methods=['GET'])
def get_ngrams_tweets():
    """."""
    if request.args['folder'] == 'individual':
        for user in USERS_LIST:
            user_tweets_ngrams = tweets_ngrams(user,INDIVIDUAL_FOLDER)
            user_tweets_ngrams.monogramming()
            user_tweets_ngrams.ngraming()
    elif request.args['folder'] == 'batch':
        user_tweets_ngrams = tweets_ngrams('',BATCH_FOLDER)
        user_tweets_ngrams.ngraming_in_one_file(USERS_LIST)
    else:
        return "Error: Not a valid folder field provided. Please specify an folder adding at the end of the url '?folder=***'."
    return None

if __name__ == '__main__':
    app.run()

sentimiento_folder = 'sentimiento'
opinion_folder = 'opinion'
mensajes_folder = 'mensajes'

sentimiento = tweets_management(sentimiento_folder)
sentimiento.cleaning()

opinion = tweets_management(opinion_folder)
opinion.cleaning()

sorter_sentimiento = tweets_classification(sentimiento_folder)
sorter_sentimiento.training(0.1,0.9)
sorter_sentimiento.test_Naive_Bayes()
sorter_sentimiento.test_SVM()
sorter_sentimiento.test_Decision_Tree()
sorter_sentimiento.test_Max_Entropy()
sorter_sentimiento.test_batch()

sorter_opinion = tweets_classification(opinion_folder)
sorter_opinion.training(0.1,0.9)
sorter_opinion.test_Naive_Bayes()
sorter_opinion.test_SVM()
sorter_opinion.test_Decision_Tree()
sorter_opinion.test_Max_Entropy()
sorter_opinion.test_batch()

n_grams_sentimiento = tweets_ngrams(sentimiento_folder)
n_grams_sentimiento.monogramming()
n_grams_sentimiento.ngraming()

n_grams_opinion = tweets_ngrams(opinion_folder)
n_grams_opinion.monogramming()
n_grams_opinion.ngraming()
