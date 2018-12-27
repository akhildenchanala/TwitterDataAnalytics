# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import pandas as pd
import time
import json
import dateutil.parser
from textblob import TextBlob
from pandas.core.resample import TimeGrouper
from pandas.tseries.offsets import DateOffset
#from cachetools import cached, TTLCache  # 1 - let's import the "cached" decorator and the "TTLCache" object from cachetools
#cache = TTLCache(maxsize=1000, ttl=300)

###############################################################
#This functions will return the data as required by google maps
def make_maps(tweetsDataframe):

	sentiment_map = []
	retweet_table = []

########################################
##for the sentiment_map plot :: geochart
	for i in range(0,len(tweetsDataframe)):

		temp= []
		latitude = tweetsDataframe['latitude'][i]
		longitude = tweetsDataframe['longitude'][i]
		sentiment = tweetsDataframe['sentiments'][i]
		#country = tweetsDataframe['country'][i]
		
		if latitude != 0:
			temp = [latitude,longitude,sentiment]
			sentiment_map.append(temp)
		else:
			continue
########################################



########################################
#Most Famous Tweet Table :: Table_Chart
	retweet_table.append(["Tweet Author","ReTweets"])
	df = tweetsDataframe[['user','retweet_count']].drop_duplicates().sort_values(['retweet_count'],ascending=False)[:40]
	for key,value in zip(df['user'],df['retweet_count']):
		temp = [key,value]
		retweet_table.append(temp)

	return (sentiment_map,retweet_table)
########################################

	
########################################
#for the Trend Line : trend_line
def make_trend_line(tweetsDataframe):

	trends =[]
	data = []
	trend_line = []	
	file = pd.read_csv('./data/trends/trends.csv')

	trends.append('Time')
	for id,row in file.iterrows():
		location = row[0]
		trends.append(location)

	for id,row in tweetsDataframe.iterrows():
		d = dateutil.parser.parse(str(id)).date()
		data.append([(str(d)),(row[0]),(row[1]),(row[2]),(row[3]),(row[4]),(row[5]),(row[6]),(row[7]),(row[8]),(row[9]),(row[10]),(row[11]),(row[12]),(row[13]),(row[14])])
	trend_line.append(trends)
	trend_line.extend(data)

	return trend_line
########################################	
	
########################################
#for the Hashtags
def make_hashtags(tweetsDataframe):

	hashtags = []
	hashtags.append(["Trend"])
	df = tweetsDataframe['trends'].drop_duplicates()[:40]
	
	for value in df:
		hashtags.append([value])
	return hashtags
########################################
		

	
#@cached(cache)
def Twitter(search_string):
	
	graph = pd.read_csv('./data/trends_flow/graph.csv')
	graph.set_index('created_at', inplace=True)
	trends = pd.read_csv('./data/trends/trends.csv')
	file_path = str("./data/hashtags/") + str(search_string) + str(".csv")
	data = pd.read_csv(file_path, low_memory = False)
	tweet_Data = filter_tweets(data)
	trend_line = make_trend_line(graph)
	trends = make_hashtags(trends)
	sentiment_map,retweet_table = make_maps(tweet_Data)
	
	return (sentiment_map,retweet_table,trend_line,trends)
	
def Trends():

	trends = pd.read_csv('./data/trends/trends.csv')
	trend_line = make_hashtags(trends)
	
	return trend_line
	


def filter_tweets(tweets):

	id_list = tweets['id']
	tweet_Data = pd.DataFrame(id_list,columns=['id'])
	tweet_Data['user'] = tweets['user']
	tweet_Data['text'] = tweets['text']
	tweet_Data['retweet_count'] = tweets['retweet_count']
	tweet_Data['location'] = tweets['location']
	tweet_Data["latitude"] = tweets['latitude']
	tweet_Data["longitude"]= tweets['longitude']
	tweet_Data["country"] = tweets['country']
	tweet_Data["sentiments"] = tweets['sentiments']
	tweet_Data = tweet_Data.fillna(0)
	
	return tweet_Data


	
