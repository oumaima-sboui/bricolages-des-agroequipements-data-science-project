##Ce fichier python sert à extraire les sous_titrages des vidéos d'un ensemble
##de liens et les stockées dans un fichier text

from youtube_transcript_api import YouTubeTranscriptApi
import csv
from datetime import datetime
import time
import glob
from pytube import YouTube
 


now=datetime.now()
string_i_want=('%02d:%02d.%d'%(now.minute,now.second,now.microsecond))[:-4]
print("start",string_i_want) 
file = open('liens.txt', "r") 
lines = file.readlines()

for line in lines:
  trans = True 
  
  yt = YouTube(line)
  
  try:
      # using the srt variable with the list of dictonaries
      # obtained by the the .get_transcript() function
      srt = YouTubeTranscriptApi.get_transcript(str(yt.video_id) ,languages=['fr','en'])
  except:
      trans = False
      
  # creating or overwriting a file "subtitles.txt" with
  # the info inside the context manager
  with open("subtitle.txt", "a") as f:
      f.write("\n{}".format(line))
      # iterating through each element of list srt
      
      
      if (trans == False ):
          f.write("cette video n'a pas de transcription\n")
          continue 
      for i in srt:
          if ((i['text'] == "[Musique]")or (i['text'] == "[Music]")) :
               
              i['text'] = "*****"
              
          if ((i['text'] == "[Applause]") or (i['text'] == "[Applaudissements]")):
              i['text'] = ""
              
          else :
              f.write("\n{}".format(i['text']))

