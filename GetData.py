import tweepy
from pymongo import MongoClient
import json
import os
import time
import sys 
from Timeline import getUserTimeline

client = MongoClient()
db = client.AB_Revision
users_db = client.IDs
AUTH_KEYS = []



# General helper function for initAuthKeys. This adds the authenticated key to AUTH_KEYS
# for the program to use later. Currently, this does not work. I get an exception trying to use
# multiple keys at once. 
def authenticate(listWithAuthKeys):
	auth = tweepy.OAuthHandler(listWithAuthKeys[0], listWithAuthKeys[1])
	auth.set_access_token(listWithAuthKeys[2], listWithAuthKeys[3])
	AUTH_KEYS.append(tweepy.API(auth))

# Function will init the auth keys recursively and throw a "Used all keys." Error message when it 
# has stepped through all of the auth keys in the secrets.json file.
def initAuthKeys(keyCount):
	try:
		with open('secrets.json', 'r') as f:
			data = json.load(f)
			CKEY = data["auth" + str(keyCount)]["CKEY"]
			CSECRET = data["auth" + str(keyCount)]["CSecret"]
			AKEY = data["auth" + str(keyCount)]["AToken"]
			ASECRET = data["auth" + str(keyCount)]["ASecret"]
			key = [CKEY, CSECRET, AKEY, ASECRET]
			authenticate(key)
			initAuthKeys(keyCount + 1)
	except KeyError:
		print("Used all keys.")

# This function takes information from getUserOneLevel and formats it into a python dictionary
# which MongoDB will gladly accept and insert into the database.
def formatJson(id, fList, field):
	user = {"TID" : str(id)}
	user[str(field)] = {}
	for i, value in enumerate(fList):
		user[field][str(i)] = str(value)
	return user

# Given an originaly user (passed from main), this function will collect all of 
# the followers and people following of every single person in relation to the original user.
def getFollowing(follower, api):
	try:
		print("Getting people " + str(follower) + " follows.")
		followingList = []
		dbCollectionName = "info_" + str(follower) 
		for page in tweepy.Cursor(api.friends_ids, id = follower).pages(1):
			followingList.extend(page)
			time.sleep(61)
		db[dbCollectionName].insert_one(formatJson(follower, followingList, "following"))
	except TweepError:
		print("Follower " + str(follower) + " didn't complete.")

def fetchAndInsertFollowingsUserDB(twitterIDSList):
	#Creates sublists of length 100 of all of IDS
	subLists = [twitterIDSList[x:x+100] for x in range(0, len(twitterIDSList), 100)]
	#Iterates over the lists of 100
	for userList in subLists:
		try:
			page = AUTH_KEYS[0].lookup_users(user_ids=userList)
			users_db["user_information"].insert_many(page)
			print("Finished Batch Insert of followings per follower")
			time.sleep(60)
		except TweepError:
			print("Protected User FollowignsUserDB")
#Receives a list of all the collections and chops it up into sublists of 100 each.
def fetchAndInsertCollectionUserDB(twitterIDSList):
	collectionsGroup100 = [twitterIDSList[x:x+100] for x in range(0, len(twitterIDSList), 100)]
	
	#Iterates over the sublists
	for userLists in collectionsGroup100:
		#user is the twitterID of the people in the collections.
		#Here is where we would want to get all of the followers of a user.
		for user in userLists:
			collLookup = "info_" + user
			print(collLookup)
			temp = []
			for key,value in db[collLookup].find_one()['following'].items():
				temp.append(value)
			fetchAndInsertFollowingsUserDB(temp)
		try:
			page = AUTH_KEYS[0].lookup_users(user_ids=userLists)
			users_db["user_information"].insert_many(page)
		except:
			print("Protected User")
if __name__ == '__main__':
	
	lookupTerm = sys.argv[1]
	dbCollectionName = "info_" + lookupTerm
	
	initAuthKeys(0)

	# getUserTimeline is implemented and works, however I haven't implemented it into this code yet.
	# Simply call the function with the (<ID YOU WANT TO SEARCH>, <AUTH KEY YOU WANT TO USE>) and it will return
	# the raw data of the user's metadata, and 20 most recent tweets.
	#print(getUserTimeline(lookupTerm, AUTH_KEYS[0]))

	#Get initial following/follower list of user entered. 
	followerIDS = []
	CKEY = ""
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
	#api = AUTH_KEYS[0]
	print("CKEY: " + str(CKEY) + "\n" + "CSECRET: " + str(CSECRET) + "\nAKEY: " + str(AKEY) + "\nASECRET" + str(ASECRET))
	auth = tweepy.OAuthHandler(CKEY, CSECRET)
	auth.set_access_token(AKEY, ASECRET)
	api = tweepy.API(auth)
		
		
	for page in tweepy.Cursor(AUTH_KEYS[0].followers_ids, id=lookupTerm).pages(1):
		print("Getting followers for " + str(lookupTerm))
		followerIDS.extend(page)
		time.sleep(61)
		
	db[dbCollectionName].insert_one(formatJson(lookupTerm, followerIDS, "followers"))
	for follower in followerIDS:
		getFollowing(follower, AUTH_KEYS[0])	
	
	collections = db.collection_names(include_system_collections=False)
	for i,user in enumerate(collections):
		collections[i] = str(user[5:])
	
	#Gets all of the user profiles for every person in the collection in the db,
	#Then gets all of the people each of those users are following's accounts."
	fetchAndInsertCollectionUserDB(collections)	
	
