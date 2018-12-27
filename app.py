from flask import Flask, render_template,request
from tweets import Twitter
import json

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
	if request.method == "GET":
		search = "2017"
		(a,b,c,d)=Twitter(search)
		print(a,b,c,d)
		return render_template('home.html',tweet_map=a,retweet_table=json.dumps(b),trend_line=(c),hashtags = json.dumps(d),search=search)
	else:	

		search = request.form["select"]
		print(search)
		(a,b,c,d)=Twitter(search)
		print(a,b,c,d)
		return render_template('home.html',tweet_map=a,retweet_table=(b),trend_line=(c),hashtags = json.dumps(d),search=search)
	return "<h1>Something went wrong !! </h1>"



if __name__ == "__main__":
	app.run()
	
