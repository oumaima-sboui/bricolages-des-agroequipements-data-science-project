

##Ce fichier python sert à extraire les données d'une page YouTube d'une liste des
##liens et les stockées dans une fichier csv


# importing modules
from pytube import YouTube
import csv
from datetime import datetime
import time
import glob

now=datetime.now()
string_i_want=('%02d:%02d.%d'%(now.minute,now.second,now.microsecond))[:-4]
print("start",string_i_want) 
file = open('liens.txt', "r") 
lines = file.readlines()

for line in lines:
  
  yt = YouTube(line)
  with open('info_youtube.csv', 'a',encoding="utf-8-sig") as f:
    fieldnames = ['title','number_of_views','duration','description','publish_date','author',"channel_id","channel_url","keywords","id"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    #writer.writeheader()
    writer.writerow({'title':str(yt.title),
                   'number_of_views':str(yt.views),
                   'duration': str(yt.length),
                   'description':str(yt.description),
                   'publish_date':str(yt.publish_date),
                   'author':str(yt.author),
                   "channel_id":str(yt.channel_id),
                   "channel_url":str(yt.channel_url),
                   "keywords":str(yt.keywords),
                   "id":str(yt.video_id)})
now=datetime.now()
string_i_want=('%02d:%02d.%d'%(now.minute,now.second,now.microsecond))[:-4]
print ("end=",string_i_want)


      
#Download Scraped Video
#video = yt.streams.get_highest_resolution()
#video.download()



 


