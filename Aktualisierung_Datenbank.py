# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:15:57 2018

@author: David
"""

import tweepy
import csv
import pandas as pd
import datetime as dt
consumer_key="secret"
consumer_secret="secret"
access_token="secret"
access_token_secret="secret"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


auslassen=['@ademov_eu', '@hans_van_baalen', '@MarioBorghezio', '@JcolombierFN', '@Albert_Dess_MEP',
           '@BillDudleyNorth', '@raymondfinch', '@JFlackMEP', '@michaelgahler', '@ngriesbeck', 
           '@JametFrance', '@TeresaJBecerril', '@LanciniOscar', '@LJManscour', '@JoelleMelinFN', 
           '@Nuno_Melo_CDSPP', '@paulnuttallukip', '@libertarofuturo', '@robertrochefort', 
           '@PaulRuebig', '@JLSchaffhauser', '@schiderwan', '@MollyScottCato', '@AnnaZaborska',"@TraianUngureanu"]



#für die (tägliche) Aktualisierung der Datenbank:
df=pd.read_csv("MyPath.csv")
parlamentarier=df[df["SCREEN_NAME"].notnull()]
tweets_df=pd.read_csv("MyPath_tweets.csv",usecols=[1],delimiter=";")
csvFile = open('MyPath.csv', 'a',newline='',encoding="utf-8")
csvWriter = csv.writer(csvFile,delimiter=';')

alle_politiker=parlamentarier["SCREEN_NAME"].values
alle_länder=parlamentarier["NATIONALITY"].values
alle_parteien=parlamentarier["GROUP"].values
problem_politiker=[]
all_new_tweets=0

for counter,politiker in enumerate(zip(alle_politiker,alle_länder,alle_parteien)):
    if politiker[0] not in auslassen:
        try:
            tweets=api.user_timeline(screen_name =politiker[0],count=100, include_rts = True,tweet_mode='extended') #8min for count=50 - sometimes not enough -> after brexit deal
            count_tweet=0
            for tweet in tweets:
                if tweet.id not in tweets_df["id"].values:
                    csvWriter.writerow([
                        tweet.created_at, tweet.id_str, politiker[1], politiker[2],tweet.user.screen_name,tweet.user.name ,tweet.author.name,tweet.user.followers_count,
                        tweet.in_reply_to_screen_name,tweet.in_reply_to_status_id_str,tweet.is_quote_status,tweet.retweet_count,
                        tweet.favorite_count,tweet.lang,
                        tweet.full_text, tweet.entities["hashtags"],tweet.entities['urls'],
                        tweet.entities['user_mentions']])
    
                    count_tweet+=1
                    all_new_tweets+=1
            print(str(counter+1)+"/"+str(len(alle_politiker)),politiker[0],": \t \t "+str(count_tweet)+" neue Tweets")
        except:
            print("Name nicht gefunden")
            problem_politiker.append(politiker[0])
            next
print()
print("Aktualisierung Tweets beendet")
print("neue Tweets gesamt: ",all_new_tweets)

print(problem_politiker)
csvFile.close()
print()
print("Aktualisierung der Trending Hashtags Datenbank...")
hashtags=pd.read_csv('MyPath_hashtags.csv',delimiter=";")
hashtags["uhrzeit_scrape"]=pd.to_datetime(hashtags["uhrzeit_scrape"])
if dt.datetime.now()-hashtags["uhrzeit_scrape"].iloc[-1]>dt.timedelta(minutes=2):
    places={
            "Deutschland": 23424829,"Irland": 23424803,"Österreich": 23424750, "Belgien": 23424757,
            "Dänemark": 23424796, "Frankreich": 23424819,"Griechenland": 23424833, "Italien": 23424853,
            "Lettland": 23424874, "Niederlande": 23424909,	"Polen": 23424923, "Portugal": 23424925,
            "Schweden": 23424954,"Spanien": 23424950, "UK":	23424975	
            }
    csvFile = open('MyPath_hashtags.csv', 'a',newline='',encoding="utf-8")
    csvWriter = csv.writer(csvFile,delimiter=';')
    for place in places.keys():
        trends=api.trends_place(places[place])[0]['trends']
        for hashtag in trends:
            csvWriter.writerow([
                place,dt.datetime.now(),hashtag["name"]])
        print(place)
    csvFile.close()
else:
    print("Hashtags wurden innerhalb der letzten 3h bereits aktualisiert")
print("Aktualisierungen beendet")
input("Bitte 'Enter' betätigen zum Beenden des Programmes")