from flask import Flask, render_template,request
from tweets import Twitter
import pandas as pd
import json

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
	if request.method == "GET":
		return render_template('home.html')

	else:
		search = request.form["srch-term"]
		(a,b,c,d,e)=Twitter(search)
		return render_template('home.html',doughnut=json.dumps(a),tweet_map=b,sources_plot=json.dumps(c),sentiment_pie=json.dumps(d),table=json.dumps(e),search=search)

	return "<h1>Something went wrong !! </h1>"



if __name__ == "__main__":
	app.run(debug=True,port = 8000)
	
