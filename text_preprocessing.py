import nltk
import csv
import chardet
import pandas as pd
from nltk.corpus import stopwords
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
import spacy

#Load the spacy stop word en francais et creation du my custum stopword
nlp = spacy.load('fr_core_news_sm')
doc= nlp("bonjour faire bien  notification Pourquoi Coucou tout le monde à tous Hola abonnez abonne salut  j aime lien  site  notre  attention  merci  hésitez pas poser vos questions à toutes et à tous  vous entendez bienvenue  au revoir contacter pardon trés beau  télephone  rendez-vous par email  video non mienne  oh  bonne journée  remercie  en plus webinare")
                 

empty_list = []
for token in doc:
    empty_list.append(token.lemma_)

final_custom_stop_word_fr = ' '.join(map(str,empty_list))
#print(final__custom_stop_word_fr)
#print(final__custom_stop_word_en)



# mettre en minuscules + enlever les ponctuaion

with open('sous_titrage.csv', 'rb') as f:
    enc = chardet.detect(f.read())  # or readline if the file is large  
df = pd.read_csv('sous_titrage.csv', encoding = enc['encoding'])
df_text=df[['sous_titrage']]
#print (df_text.head())


    
#Lowercasing

df_text['sous_titrage']=df_text['sous_titrage'].str.lower()
#print(df_text.head())



#Remove Extra Whitespaces

def remove_whitespace(text):
    return  " ".join(text.split())
df_text['sous_titrage']=df['sous_titrage'].apply(remove_whitespace)
#print(df_text['sous_titrage'])


#word tokonizer
from nltk import word_tokenize
df_text['sous_titrage']=df_text['sous_titrage'].apply(lambda X: word_tokenize(X))
#print(df_text.head())




# Removing Punctuations
from nltk.tokenize import RegexpTokenizer
def remove_punct(text):
    
    tokenizer = RegexpTokenizer(r"\w+")
    lst=tokenizer.tokenize(' '.join(text))
    return lst

df_text['sous_titrage'] = df_text['sous_titrage'].apply(remove_punct)



#lemmatization 
def lemmatization(text):  # clean up your text and generate list of words for each document. 
    
    text_out = []
    doc= nlp(text)
    for token in doc:
        if token.is_stop == False and token.is_alpha and len(token)>2 and token.pos_ not in final_custom_stop_word_fr:
            lemma = token.lemma_
            text_out.append(lemma)
            
    return text_out
    
#datalist = data.text.apply(lambda x:clean_up(x))
df_text['sous_titrage'] = df['sous_titrage'].apply(lambda x:lemmatization(x))




#Spelling Correction

from spellchecker import SpellChecker
def spell_check(text):
    
    result = []
    spell = SpellChecker()
    for word in text:
        correct_word = spell.correction(word)
        #print(correct_word)
        result.append(correct_word)
    
    return result

df_text['sous_titrage'] = df_text['sous_titrage'].apply(spell_check)
print(df_text['sous_titrage'])

## Removing stopWOrd

def remove_stopwords(text):
    final_stopwords_list = list(fr_stop) 
    ###print(len(final_stopwords_list))
    final_stopwords_list.extend(final_custom_stop_word_fr)
    result = []
    new_text = ""
    for token in text:
        if token not in final_stopwords_list:
            #print(token)
            result.append(token)
    new_text = " ".join(result)
    #print(new_text)
    return new_text
df_text['sous_titrage'] = df_text['sous_titrage'].apply(remove_stopwords)








#Frequent Words

from nltk import FreqDist

def frequent_words(df):
    
    lst=[]
    for text in df.values:
        lst+=text[0]
    fdist=FreqDist(lst)
    return fdist.most_common(10)



    
print(df_text['sous_titrage'][0])
df_text.to_csv('sous_titrage_cleaned.csv',index = False)
