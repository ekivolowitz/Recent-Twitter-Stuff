import tweepy
from pymongo import MongoClient
import json
import os
import time
import sys 


client = MongoClient()
db = client.IDs



# This function will get the metadata of a given user, and then get their 20 newest tweets.
# This appears to be the best way to get tweets from a given user, however I am still
# looking for a better option. 
def getUserTimeline(userID, api):	
	'''
	CSECRET = ""
	AKEY = ""
	ASECRET = ""
	keyCount = 0	 
	with open('secrets.json', 'r') as f:
		data = json.load(f)
		CKEY = data["auth" + str(keyCount)]["CKEY"]
		CSECRET = data["auth" + str(keyCount)]["CSecret"]
		AKEY = data["auth" + str(keyCount)]["AToken"]
		ASECRET = data["auth" + str(keyCount)]["ASecret"]
	auth = tweepy.OAuthHandler(CKEY, CSECRET)
	auth.set_access_token(AKEY, ASECRET)
	api = tweepy.API(auth)
	'''
	userResponse = api.user_timeline(userID)
	return userResponse
