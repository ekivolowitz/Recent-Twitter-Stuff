import tweepy
from pymongo import MongoClient
import json
import os
import time
import sys 


client = MongoClient()
db = client.IDs

#def getUserFollowers(follower, api):
	#print("Getting info for " + str(follower))
	#followerIDS = []
	#followingIDS = []
	#dbCollectionName = "info_" + str(follower) 
	#for page in tweepy.Cursor(api.followers_ids, id = follower).pages(1):
	#	followerIDS.extend(page)
	#	time.sleep(61)
	
	#for page in tweepy.Cursor(api.followers_ids, id = follower).pages(1):
	#	followingIDS.extend(page)
	#	time.sleep(61)
	#db[dbCollectionName].insert_one(formatJson(follower, followerIDS, followingIDS))
		

if __name__ == '__main__':	
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
	userResponse = api.user_timeline("therealkibbles")
	print(userResponse)
