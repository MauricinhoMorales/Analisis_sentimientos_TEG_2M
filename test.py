from flask import Flask
from IPython.display import display
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)

df = pd.read_csv('Tweets_Clasificados.csv')

display(df.head(69))
