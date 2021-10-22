"""."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:26444352m@localhost/TEG2Mv0.1'
app.debug = True
db = SQLAlchemy(app)

class TweetsModel(db.Model):
    """."""
    __tablename__ = 'tweets_model'

    tweet_id = db.Column(db.String, primary_key=True)
    tweet_date = db.Column(db.String)
    tweet_username = db.Column(db.String)
    tweet = db.Column(db.String)
    tweet_translated = db.Column(db.String)
    tweet_sentiment = db.Column(db.String)
    tweet_opinion = db.Column(db.String)
    tweet_tokenized = db.Column(db.String)
    tweet_translated_tokenized = db.Column(db.String)

    def __init__(self,tweet_id,tweet_date,tweet_username,
            tweet,tweet_translated,tweet_sentiment,tweet_opinion,
            tweet_tokenized,tweet_translated_tokenized):
        self.tweet_id = tweet_id
        self.tweet_date = tweet_date
        self.tweet_username = tweet_username
        self.tweet = tweet
        self.tweet_translate = tweet_translated
        self.tweet_sentiment = tweet_sentiment
        self.tweet_opinion = tweet_opinion
        self.tweet_tokenized = tweet_tokenized
        self.tweet_translated_tokenized = tweet_translated_tokenized

class TweetsModelSentimient(db.Model):
    """."""
    __tablename__ = 'tweets_model_sentiment'

    tweet_id = db.Column(db.String, primary_key=True)
    tweet = db.Column(db.String)
    tweet_tokenized = db.Column(db.String)
    tweet_translated = db.Column(db.String)
    tweet_translated_tokenized = db.Column(db.String)
    tweet_sentiment = db.Column(db.String)

    def __init__(self,tweet_id,tweet,tweet_tokenized,tweet_translated,
            tweet_translated_tokenized,tweet_sentiment):
        self.tweet_id = tweet_id
        self.tweet = tweet
        self.tweet_tokenized = tweet_tokenized
        self.tweet_translated = tweet_translated
        self.tweet_translated_tokenized = tweet_translated_tokenized
        self.tweet_sentiment = tweet_sentiment

class TweetsModelOpinion(db.Model):
    """."""
    __tablename__ = 'tweets_model_opinion'

    tweet_id = db.Column(db.String, primary_key=True)
    tweet = db.Column(db.String)
    tweet_tokenized = db.Column(db.String)
    tweet_translated = db.Column(db.String)
    tweet_translated_tokenized = db.Column(db.String)
    tweet_opinion = db.Column(db.String)

    def __init__(self,tweet_id,tweet,tweet_tokenized,tweet_translated,
            tweet_translated_tokenized,tweet_opinion):
        self.tweet_id = tweet_id
        self.tweet = tweet
        self.tweet_tokenized = tweet_tokenized
        self.tweet_translate = tweet_translated
        self.tweet_translated_tokenized = tweet_translated_tokenized
        self.tweet_opinion = tweet_opinion

class TweetsTestModel(db.Model):
    """."""
    __tablename__ = 'tweets_test'

    tweet_id = db.Column(db.String, primary_key=True)
    tweet_date = db.Column(db.String)
    tweet_username = db.Column(db.String)
    tweet = db.Column(db.String)
    tweet_translated = db.Column(db.String)
    tweet_sentiment = db.Column(db.String)
    tweet_opinion = db.Column(db.String)
    tweet_tokenized = db.Column(db.String)
    tweet_translated_tokenized = db.Column(db.String)

    def __init__(self,tweet_id,tweet_date,tweet_username,
            tweet,tweet_translated,tweet_sentiment,tweet_opinion,
            tweet_tokenized,tweet_translated_tokenized):
        self.tweet_id = tweet_id
        self.tweet_date = tweet_date
        self.tweet_username = tweet_username
        self.tweet = tweet
        self.tweet_translated = tweet_translated
        self.tweet_sentiment = tweet_sentiment
        self.tweet_opinion = tweet_opinion
        self.tweet_tokenized = tweet_tokenized
        self.tweet_translated_tokenized = tweet_translated_tokenized

class StadisticsModel(db.Model):
    """."""
    __tablename__ = 'stadistics'

    stadistic_id = db.Column(db.String, primary_key=True)
    stadistic_accuracy = db.Column(db.Float)
    stadistic_precision = db.Column(db.Float)
    stadistic_recall = db.Column(db.Float)
    stadistic_f1_score = db.Column(db.Float)
    stadistic_accuary_all = db.Column(db.Float)
    stadistic_precisio_all = db.Column(db.Float)
    stadistic_recall_all = db.Column(db.Float)
    stadistic_f1_score_all = db.Column(db.Float)

    def __init__(self,stadistic_id,stadistic_accuracy,stadistic_precision,
            stadistic_recall,stadistic_f1_score,stadistic_accuary_all,
            stadistic_precisio_all,stadistic_recall_all,stadistic_f1_score_all):
        self.stadistic_id = stadistic_id
        self.stadistic_accuracy = stadistic_accuracy
        self.stadistic_precision = stadistic_precision
        self.stadistic_recall = stadistic_recall
        self.stadistic_f1_score = stadistic_f1_score
        self.stadistic_accuary_all = stadistic_accuary_all
        self.stadistic_precisio_all = stadistic_precisio_all
        self.stadistic_recall_all = stadistic_recall_all
        self.stadistic_f1_score_all = stadistic_f1_score_all