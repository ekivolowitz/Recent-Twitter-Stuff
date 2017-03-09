#created by Song Wang Mar 8, 2017
# this script will read in a adjlist separated by comma, output a edgelist and write that into a csv file

# coding: utf-8


import csv
import re

class createBipFromFriendlist(object):
    
    def __init__(self, threshold = 5):
        """
        adjlist type: list[list] first item is follower_id, the rest are the IDs of its friends
        rtype : None
        """
        self.adjlist = None
        self.friendsCount = None
        #self.edgelist = []  #only keep  
        #self.reducedAdjlist = []
        
    def createAdjlist(self, input_file, verbose = True):
        """
        : type input_file: list[str] 
        a text file name, each row is a string 
        starting with a screen_name, and a list of id_str's  of his fiends, separated by ','
        : rtype : list[list]
         remove some rows, with 0 friends or have 'NA' as their friends, which indicates 
                    downloading unsucessfully
        """

        f = open(input_file, "r")
        adjlist = []
        failed_sn = []
        zero_sn = []
        #removed those having 0 friends, 
        #removed those having 'NA' as friends -- did not download friends list sucessfullly,
        for line in f:
            a = line.split(',')
            a =[re.sub("\n", "", x) for x in a]
            if len(a) == 1:
                zero_sn.append(a[0])
            elif len(a) ==2 and a[1] =='NA' :
                failed_sn.append(a[0]) 
            else: 
                adjlist.append(a)    #adjlist is a list[list]

        if verbose:
            print ("success>0: "+str(len(adjlist)) + ",  failed: " +str(len(failed_sn))+ ", zeros: " + str(len(zero_sn)))
        self.adjlist = adjlist

    def calculateFriendsCount(self, threshold = 1):
        """
        rtype: dict()
        key: friend IDs, values, numbers of followers in the graph
        keep the friendIds with >= self.threshold followers
        """
        friendsCount = {}
        for i in range(len(self.adjlist)):
            line = self.adjlist[i]
            for id_str in line[1:]:
                if id_str in friendsCount.keys():
                    friendsCount[id_str] = friendsCount[id_str] +1
                else:
                    friendsCount[id_str] = 1      
                    if len(friendsCount) % 1000000 ==0 :
                        print (i, len(friendsCount))
        for key in list(friendsCount.keys()):
            if friendsCount[key] < threshold:
                del friendsCount[key]
        self.friendsCount = friendsCount 
                
    def createEdgelist(self, output_file, threshold = 1):
        """
        create the edgelist from the adjlist --  write out directly to save memory&time
        type: list[list]
        list in side of [a,b] -- edge
        total length of outside list == number of edges
        """
        self.calculateFriendsCount(threshold)
        with open(output_file,'w') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['row_id','follower_id_str','friends_id_str'])
            for line in self.adjlist:
                for id_str in line[1:]:
                    if id_str in self.friendsCount.keys():
                        row = (line[0],id_str)
                        csv_out.writerow(row)
            
   
                        



"""

import csv
import time
start_time = time.time()
# your code

input_file = "../edgelist_Feb27/2.txt"
output_file = "../edgelist_Feb27/edgelist_2.csv"
BipGraph = createBipFromFriendlist()
BipGraph.createAdjlist(input_file)
BipGraph.createEdgelist(output_file, threshold = 5)

"""
