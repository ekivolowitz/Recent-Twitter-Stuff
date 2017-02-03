import tweepy
from pymongo import MongoClient
import json
import os
import time
import sys 

CKEY = ''
CSECRET = ''
AKEY = ''
ASECRET = ''


client = MongoClient()
db = client.IDs


def formatJson(id, followersList, following):
	user = {"TID" : id}
	user["followers"] = {}
	user["following"] = {}
	
	for i,value in enumerate(followersList):
		user["followers"][str(i)] = str(value)	
	for i, value in enumerate(following):
		user["following"][str(i)] = str(value)
	return user

def getUserFollowers(follower, api):
	
	followerIDS = []
	followingIDS = []
	dbCollectionName = "info_" + str(follower) 
	for page in tweepy.Cursor(api.followers_ids, id = follower).pages(1):
		followerIDS.extend(page)
		time.sleep(61)
	
	for page in tweepy.Cursor(api.followers_ids, id = follower).pages(1):
		followingIDS.extend(page)
		time.sleep(61)
	db[dbCollectionName].insert_one(formatJson(follower, followerIDS, followingIDS))

if __name__ == '__main__':
	
	lookupTerm = sys.argv[1]
	dbCollectionName = "info_" + lookupTerm

	# with open('config.json', 'r') as f:
	#     data = json.load(f)
	#     CKEY = data["auth1"]["CKEY"]
	#     CSECRET = data["auth1"]["CSecret"]
	#     AKEY = data["auth1"]["AToken"]
	#     ASECRET = data["auth1"]["ASecret"]

	auth = tweepy.OAuthHandler(CKEY, CSECRET)
	auth.set_access_token(AKEY, ASECRET)
	api = tweepy.API(auth)
	

	#Get initial following/follower list of user entered. 
	followerIDS = []
	followingIDS = []
	for page in tweepy.Cursor(api.followers_ids, id=lookupTerm).pages(1):
		followerIDS.extend(page)
		time.sleep(61)

	for page in tweepy.Cursor(api.friends_ids, id=lookupTerm).pages(1):
		followingIDS.extend(page)
		time.sleep(61)
	
		
	db[dbCollectionName].insert_one(formatJson(lookupTerm, followerIDS, followingIDS))

	for follower in followerIDS:
		getUserFollowers(follower, api)

