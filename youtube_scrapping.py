

##Ce fichier python sert à extraire les données d'une page YouTube (les métadonnées) d'une liste des
##liens et les stockées dans une fichier csv
##ce fichier sera utilisé en deux reprises avant et aprés l'executable de  filtre des liens 


# importing modules
from pytube import YouTube
from mtranslate import translate

import csv
from datetime import datetime
import time
import re
import glob
import string
now=datetime.now()
characters = "/_\[]@|~{}@!?"
def supp_special_carac (srt):
  
    for x in range(len(characters)):
      srt = srt .replace(characters[x],"")
    a=re.sub("\d\d\:\d\d|\d\d\\s:\s\d\d|\d\d\\s:\d\d|\d\d\:\s\d\d","",srt)

    return(a)




file = open('liens2.txt', "r") 
lines = file.readlines()
print(len(lines))
i=0
with open('info_youtube_2.csv', 'w',encoding="utf-8-sig") as f:
  fieldnames = ['title','number_of_views','duration','description','publish_date','author',"channel_id","channel_url","keywords","id"]
  writer = csv.DictWriter(f, fieldnames=fieldnames)
  writer.writeheader()
  for line in lines:
    yt = YouTube(line)
  
    try:
      writer.writerow({'title':str(translate(supp_special_carac(yt.title), 'fr', "auto")),
                     'number_of_views':str(yt.views),
                     'duration': str(yt.length),
                      
                     'description':translate(str.lower(supp_special_carac(yt.description)),'fr', "auto"),
                     'publish_date':str(yt.publish_date),
                     'author':str(translate(supp_special_carac(yt.author ), 'fr', "auto")),
                     "channel_id":str(yt.channel_id),
                     "channel_url":str(yt.channel_url),
                     "keywords":str(yt.keywords),
                     "id":str(yt.video_id)})
    except :
      print(line)
      print(yt.description)
    
      i=i+1
      continue
print("nombre des liens est",i)





 


