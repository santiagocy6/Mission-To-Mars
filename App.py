from flask import Flask, render_template, redirect
import pymongo
import scrape
import pandas as pd 

# Set up flask
app = Flask(__name__)
# Connect to pymongo
conn = "mongodb://localhost:27017/mars_database"
client = pymongo.MongoClient(conn)

@app.route("/")
def index():
	mars = client.db.mars.find_one()
	table = pd.read_json(mars["mars_facts"]).to_html()
	table = table.replace('<table border="1" class="dataframe">','<table class="table">')
	table = table.replace('<th>','<th scope="col">')
	return render_template("index.html", mars = mars, table = table)

@app.route("/scrape")
def scrape():
	mars = client.db.mars 
	data = scrape.scrape()
	mars.update({}, data)
	return redirect("/", code=302)

if __name__ == "__main__":
	app.run(debug=True)