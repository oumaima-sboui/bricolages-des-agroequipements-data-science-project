import nltk
import csv
import chardet
import pandas as pd
from nltk.corpus import stopwords
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
import spacy
from collections import Counter

#Load the spacy stop word en francais et creation du my custum stopword
nlp = spacy.load('fr_core_news_sm')
doc= nlp("bonjour épisode falloir hola bien \r\n  faire bien  notification Pourquoi Coucou tout le monde à tous Hola abonnez abonne salut  j aime lien  site  notre  attention  merci  hésitez pas poser vos questions à toutes et à tous  vous entendez bienvenue  au revoir contacter pardon trés beau  télephone  rendez-vous par email  video non mienne  oh  bonne journée  remercie  en plus webinare a à afin ai ainsi alain aller alors ans après attendu au aujourd aujourd'hui auquel aussi autre autres aux auxquelles auxquels avait avant avec avez avoir bien c ça car ce ceci cela celle celles celui cependant certain certaine certaines certains ces cet cette ceux chez chose chunk ci combien comme comment concernant contre d dans de debout dedans dehors déjà delà depuis derrière des dès désormais desquelles desquels dessous dessus deux devant devers devra dire divers diverse diverses doit donc dont du duquel durant elle elles en entre environ ès est et était etc été etre être eu eux excepté faire fait faut gens hélas hormis hors hui il ils j je jusqu jusque l la là laquelle le lequel les lesquelles lesquels leur leurs lorsque lui m ma mais malgré matériel me même mêmes merci mes mets mien mienne miennes miens moi moins mon moyennant n ne néanmoins ni non nos notre nôtre nôtres nous ô on ont ou où oui outre par parce parler parmi partant pas passé pendant petit peu peut plein plus plusieurs pour pourquoi près proche puisque qu quand que quel quelle quelles quels qui quoi quoique revoici revoilà s sa sans sauf savary se selon seront ses si sien sienne siennes siens sinon soi soit son sont sous suivant sur t ta te tes tien tienne tiennes tiens toi ton tous tout toute toutes très tu un une va vers veut voici voilà vos votre vôtre vôtres vous vraiment vu wav")

               

empty_list = []
for token in doc:
    empty_list.append(token.lemma_)

final_custom_stop_word_fr = ' '.join(map(str,empty_list))
#print(final_custom_stop_word_fr)
#print(final__custom_stop_word_en)



##vals = [','.join(ele) for ele in final_custom_stop_word_fr]
##print(vals)
# mettre en minuscules + enlever les ponctuaion

with open('sous_titrage.csv', 'rb') as f:
    enc = chardet.detect(f.read())  # or readline if the file is large  
file = pd.read_csv('sous_titrage.csv', encoding='utf-8-sig')
headerList = ['lien_youTube', 'sous_titrage'] 
  
file.to_csv("sous_titrage.csv", header=headerList, index=False)
df = pd.read_csv('sous_titrage.csv', encoding='utf-8-sig')
df1= df.dropna()
df_text=df1[['sous_titrage']]

print (df_text.head())


    
#Lowercasing

df_text['sous_titrage']=df_text['sous_titrage'].str.lower()
#print(df_text.head())



#Remove Extra Whitespaces

def remove_whitespace(text):
    
    return  " ".join(str(text).split())
df_text['sous_titrage']=df_text['sous_titrage'].apply(remove_whitespace)
#print(df_text['sous_titrage'])

df_text['text_complet']=df_text['sous_titrage']
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



#df_text.to_csv('sous_titrage_lemma.csv', mode='w', index=False ,encoding='utf-8-sig')



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
df_text['sous_titrage'] = df_text['sous_titrage'].apply(lambda x:lemmatization(x))
df_text=df_text.dropna()




#Spelling Correction
##
##from spellchecker import SpellChecker
##def spell_check(text):
##    
##    result = []
##    spell = SpellChecker()
##    for word in text:
##        correct_word = spell.correction(word)
##        #print(correct_word)
##        result.append(correct_word)
##    
##    return result
##
##df_text['sous_titrage'] = df_text['sous_titrage'].apply(spell_check)
##print(df_text['sous_titrage'])

## Removing stopWOrd










#Frequent Words

from nltk import FreqDist

def frequent_words(df):
    
    lst=[]
    for text in df.values:
        lst+=text[0]
    fdist=FreqDist(lst)
    return fdist.most_common(10)



    
print(df_text['text_complet'][0])

x = df_text.to_string(header=False,
                  index=False,
                  index_names=False).split('\n')
vals = [','.join(ele.split()) for ele in x]


#print(vals)


# We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
##from sklearn.feature_extraction.text import CountVectorizer
##
##cv = CountVectorizer(vals)
##data_cv = cv.fit_transform(df_text.sous_titrage)
##data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
##data_dtm.index = df_text.index
##print(data_dtm)
##data_dtm.to_pickle("dtm.pkl")
##
### Let's also pickle the cleaned data (before we put it in document-term matrix format) and the CountVectorizer object
import pickle
df_text.to_pickle('data_clean_final.pkl')
#pickle.dump(cv, open("cv.pkl", "wb"))
