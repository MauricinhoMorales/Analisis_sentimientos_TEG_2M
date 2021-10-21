import flask
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:26444352m@localhost/TEG2Mv0.1'
app.debug = True
db = SQLAlchemy(app)

class tweets(db.Model):
    __tablename__ = 'tweets'

    tweet_id = db.Column(db.String(100), primary_key=True)
    tweet_date = db.Column(db.String(100))
    tweet_username = db.Column(db.String(100))
    tweet = db.Column(db.String(100))
    tweet_translate = db.Column(db.String(100))
    tweet_sentiment = db.Column(db.String(100))
    tweet_opinion = db.Column(db.String(100))

    def __init__(self,tweet_id,tweet_date,tweet_username,tweet,tweet_translate,tweet_sentiment,tweet_opinion):
        self.tweet_id = tweet_id
        self.tweet_date = tweet_date
        self.tweet_username = tweet_username
        self.tweet = tweet
        self.tweet_translate = tweet_translate
        self.tweet_sentiment = tweet_sentiment
        self.tweet_opinion = tweet_opinion

@app.route('/api', methods=['GET','POST'])
def test_route():
    if flask.request.method == 'POST':
        return {
            'method':'POST'
        }
    elif flask.request.method == 'GET':
        return {
            'method':'GET'
        }

@app.route('/tweets', methods=['GET','POST'])
def tweets_route():

    if flask.request.method == 'GET':
        all_tweets = tweets.query.all()
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
        tweet_new = tweets(
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

if __name__ == '__main__':
    app.run()
