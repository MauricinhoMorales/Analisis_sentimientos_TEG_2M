from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:26444352m@localhost/TEG2Mv0.1'
app.debug = True
db = SQLAlchemy(app)

class TweetsModel(db.Model):
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