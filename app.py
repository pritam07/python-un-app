import os
from flask import Flask, jsonify, json, request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'hi'

db = SQLAlchemy(app)

class Details(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(5000), unique=True, nullable=False)

    def __init__(self, description):
        self.description = description

@app.route("/api")
def welcome():
   return "US Population API"

@app.route('/api/rules/about')
def about():
   item = Details.query.all()
   if len(item) == 1:
    response = item[0].to_dict()
   return response

@app.route('/api/getMenu')
def getMenu():
   locale = request.args.get('locale')
   if locale =='en':
      SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
      json_url = os.path.join(SITE_ROOT, "static\data", "menu.json")
      menu = json.load(open(json_url))
      return menu
   else: 
      return {"message": "You did not provided locale=en query parameter"}
   

@app.route('/api/rules/us_population')
def getPopulation():
   url = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
   response = requests.get(url)
   response = response.json()
   return response

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)