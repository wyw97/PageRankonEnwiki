#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 20:27:12 2018

@author: wangyiwen
"""

import gensim.corpora.wikicorpus as WIKI
import numpy as np
import time
import matplotlib.pyplot as plt

file_name="enwiki-20180920-pages-articles-multistream.xml"

file_path="/home/wyw/wyw/"
#lab's path
# file_path="/Volumes/Seagate Backup Plus Drive/webdata/"
# my computer
xml_path=file_path+file_name
# give the location of the xml file

WordDict={}
NumDict={}
# give the dict of the word so that each word can be represented by a number
# NumDict is the reverse of the WordDict
RankScore={}
# record the score of each webpage to the other,it can be regarded as a matrix.

OutLink={}
InLink={}
#Outlink record the node that each node connect to
#Inlink record the node that each node connect from

tot_word = 0
#tot_number = 10000
tot_number = 1000000
alPha = 0.85
epoch = 50
tolerance = 10**-9
# set the proprotion and the number of links  

#this function is used to add num to a 2-d dictionary
'''
def addtwodimdict(thedict, key_a, key_b, val):
  if key_a in thedict:
    if key_b in thedict[key_a]:
        # num=thedict[key_a][key_b]
        thedict[key_a][key_b] += val
    else:    
        thedict[key_a].update({key_b: val})
  else:
    thedict.update({key_a:{key_b: val}})
'''


def PreProcessing():
    print('begin time of the program is: ',time.ctime())
    tuPle = WIKI.extract_pages(xml_path)
    global tot_word
    #read the xml file into the tuple which is read as type yield
    cnt_time = 0
    while cnt_time < tot_number:
        curr_page = next(tuPle)
        redirects = [redirect for keyword,redirect in WIKI.find_interlinks(curr_page[1]).items()]
        cnt_time += 1
       # extract the title and the redirect title
        curr_title = curr_page[0]
        if curr_title not in WordDict:
            WordDict[curr_title] = tot_word
            NumDict[tot_word]=curr_title
            tot_word += 1
        org_id = WordDict[curr_title]
        # set the id of the word
        # sum_redirect = len(redirects)
        for redirect_title in redirects:
            
            if redirect_title not in WordDict:
                WordDict[redirect_title] = tot_word
                NumDict[tot_word] = redirect_title
                #link_id = WordDict[redirect_title]
                tot_word += 1
            link_id = WordDict[redirect_title]
            if org_id not in OutLink:
                OutLink[org_id]=[]
            OutLink[org_id].append(link_id)
            if link_id not in InLink:
                InLink[link_id]=[]
            InLink[link_id].append(org_id)
            #addtwodimdict(RankScore,org_id,link_id,1/sum_redirect)
    print('end time of the pre-processing is: ',time.ctime())     
   

def PageRank():
      print('begin time of the pagerank is: ',time.ctime())
      for i in range(tot_word):
          RankScore[i]=1/tot_word
      # initial
      sum_error = 0
      for t in range(epoch):
      #Time of iteration
          cpy_score=RankScore.copy()
          for i in range(tot_word):
              if i not in InLink:
                  continue
              node_father=InLink[i]
              RankScore[i]=(1-alPha)/tot_word
              for nod_num in node_father:
                  RankScore[i] += cpy_score[nod_num]/len(OutLink[nod_num])
          lst_error = sum_error        
          sum_error = 0
          for i in range(tot_word):
              sum_error += abs(RankScore[i]-cpy_score[i])
              
          print("epoch %d :the total difference is: "%t,sum_error)
          if sum_error<tolerance:
              break;
          if abs(sum_error-lst_error) < tolerance:
              break;
      print('end time of the pagerank is: ',time.ctime())


def ShowResult():
    Final = []
    for i in range(tot_word):
        Final.append(RankScore[i])
    Final = np.array(Final)
    FinalOrder = np.argsort(Final)[::-1]
    for i in range(10):
        pnt = FinalOrder[i]
        print(pnt,NumDict[pnt],RankScore[pnt])
    
    print('End time of the program is: ',time.ctime())


PreProcessing()
PageRank()
ShowResult()             
            