import pandas as pd
import nltk
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
nltk.download('stopwords')
nltk.download('wordnet')
df=pd.read_csv('mbti_1.csv')

data_length=[]
lemmatizer=WordNetLemmatizer()
cleaned_text=[]
stop_words = set(stopwords.words('english')) # Load stop words
pers_types = ['INFP' ,'INFJ', 'INTP', 'INTJ', 'ENTP', 'ENFP', 'ISTP' ,'ISFP' ,'ENTJ', 'ISTJ','ENFJ', 'ISFJ' ,'ESTP', 'ESFP' ,'ESFJ' ,'ESTJ']
pers_types = [p.lower() for p in pers_types]

print("Cleaning The Dataset")
for sentence in tqdm(df.posts):

    sentence=sentence.lower()

    sentence=re.sub('https?://[^\s<>"]+|www\.[^\s<>"]+',' ',sentence)

    sentence=re.sub('[^0-9a-z]',' ',sentence)

    sentence = " ".join([word for word in sentence.split() if word not in stop_words]) # Remove stop words
    #print(len(sentence))

    for p in pers_types:
        sentence = re.sub(p, '', sentence)
    #print(len(sentence))

    sentence = lemmatizer.lemmatize(sentence) # Lemmatize words
    data_length.append(len(sentence.split())) #Split data, measure length of new filtered data

    cleaned_text.append(sentence)
df['posts']=cleaned_text
print(cleaned_text)
#Save the cleaned text to a csv file
df.to_csv("changed_data.csv",index=False)
