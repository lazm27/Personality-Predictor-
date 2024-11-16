import pandas as pd
import nltk
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
nltk.download('stopwords')
nltk.download('wordnet')
import pandas as pd
import re
import numpy as np
import joblib
#df=pd.read_csv('mbti_1.csv')


def preprocess_data(post):
    #data_length=[]
    lemmatizer=WordNetLemmatizer()
    #cleaned_text=[]
    stop_words = set(stopwords.words('english')) # Load stop words
    pers_types = ['INFP' ,'INFJ', 'INTP', 'INTJ', 'ENTP', 'ENFP', 'ISTP' ,'ISFP' ,'ENTJ', 'ISTJ','ENFJ', 'ISFJ' ,'ESTP', 'ESFP' ,'ESFJ' ,'ESTJ']
    pers_types = [p.lower() for p in pers_types]
    sentence= post
    print("Cleaning The Dataset")
    #for sentence in tqdm(df.posts):

    sentence=sentence.lower()

    sentence=re.sub('https?://[^\s<>"]+|www\.[^\s<>"]+',' ',sentence)

    sentence=re.sub('[^0-9a-z]',' ',sentence)

    sentence = " ".join([word for word in sentence.split() if word not in stop_words]) # Remove stop words
        #print(len(sentence))

    for p in pers_types:
        sentence = re.sub(p, '', sentence)
        #print(len(sentence))

    sentence = lemmatizer.lemmatize(sentence) # Lemmatize words
    #data_length.append(len(sentence.split())) #Split data, measure length of new filtered data

    cleaned_text= sentence
    return pd.DataFrame(data={'type': ['INFJ'], 'posts': [cleaned_text]})




def pre_process_text(data, remove_stop_words=True, remove_mbti_profiles=True):
  list_personality = []
  list_posts = []
  len_data = len(data)
  i=0
  
  for row in data.iterrows():
      # check code working 
      # i+=1
      # if (i % 500 == 0 or i == 1 or i == len_data):
      #     print("%s of %s rows" % (i, len_data))

      #Remove and clean comments
      posts = row[1].posts

      #Remove url links 
      #temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', posts)

      #Remove Non-words - keep only words
      #temp = re.sub("[^a-zA-Z]", " ", temp)

      # Remove spaces > 1
      temp = re.sub(' +', ' ', posts).lower()
      temp = re.sub("[^a-zA-Z]", " ", temp)
      #Remove multiple letter repeating words
      #temp = re.sub(r'([a-z])\1{2,}[\s|\w]*', '', temp)

      #Remove stop words
      #if remove_stop_words:
      #    temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in useless_words])
      #else:
      #    temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ')])
          
      #Remove MBTI personality words from posts
      #if remove_mbti_profiles:
      #    for t in unique_type_list:
      #        temp = temp.replace(t,"")

      # transform mbti to binary vector
      type_labelized = translate_personality(row[1].type) #or use lab_encoder.transform([row[1].type])[0]
      list_personality.append(type_labelized)
      # the cleaned data temp is passed here
      list_posts.append(temp)

  # returns the result
  list_posts = np.array(list_posts)
  list_personality = np.array(list_personality)
  return list_posts, list_personality

#list_posts, list_personality  = pre_process_text(df, remove_stop_words=True, remove_mbti_profiles=True)

# Splitting the MBTI personality into 4 letters and binarizing it

b_Pers = {'I':0, 'E':1, 'N':0, 'S':1, 'F':0, 'T':1, 'J':0, 'P':1}
b_Pers_list = [{0:'I', 1:'E'}, {0:'N', 1:'S'}, {0:'F', 1:'T'}, {0:'J', 1:'P'}]

def translate_personality(personality):
    # transform mbti to binary vector
    return [b_Pers[l] for l in personality]

#To show result output for personality prediction
def translate_back(personality):
    # transform binary vector to mbti personality
    s = ""
    for i, l in enumerate(personality):
        s += b_Pers_list[i][l]
    return s

#list_personality_bin = np.array([translate_personality(p) for p in data.type])
#print("Binarize MBTI list: \n%s" % list_personality_bin)
    



def final(my_posts):
    #my_posts = """ They act like they care They tell me to share But when I carve the stories on my arm The doctor just calls it self harm I’m not asking for attention There’s a reason I have apprehensions I just need you to see What has become of me||| I know I’m going crazy But they think my thoughts are just hazy When in that chaos, in that confusion I’m crying out for help, to escape my delusions||| Mental health is a state of mind How does one keep that up when assistance is denied All my failed attempts to fight the blaze You treat it like its a passing phase||| Well stop, its not, because mental illness is real Understand that we’re all not made of steel Because when you brush these issues under the carpet You make it seem like its our mistake we’re not guarded||| Don’t you realise that its a problem that needs to be addressed Starting at home, in our nest Why do you keep your mouths shut about such things Instead of caring for those with broken wings||| What use is this social stigma When mental illness is not even such an enigma Look around and you’ll see the numbers of the affected hiding under the covers ||| This is an issue that needs to be discussed Not looked down upon with disgust Mental illness needs to be accepted So that people can be protected ||| Let me give you some direction People need affection The darkness must be escaped Only then the lost can be saved||| Bring in a change Something not very strange The new year is here Its time to eradicate fear||| Recognise the wrists under the knives To stop mental illness from taking more lives Let’s break the convention Start ‘suicide prevention’.||| Hoping the festival of lights drives the darkness of mental illness away"""

    # The type is just a dummy so that the data prep function can be reused
    #mydata = pd.DataFrame(data={'type': ['INFJ'], 'posts': [my_posts]})
    cleaned_text=preprocess_data(my_posts)

    my_posts, dummy  = pre_process_text(cleaned_text, remove_stop_words=True, remove_mbti_profiles=True)
    cntizer = joblib.load('models/count_vectorizer.pkl')

    tfizer = joblib.load('models/tfidf_transformer.pkl')

    my_X_cnt = cntizer.transform(my_posts)
    my_X_tfidf =  tfizer.transform(my_X_cnt).toarray()
    # Load the SVM model
    svm_model_IE = joblib.load('models/model_0.joblib')
    svm_model_NS = joblib.load('models/model_1.joblib')
    svm_model_FT = joblib.load('models/model_2.joblib')
    svm_model_JP = joblib.load('models/model_3.joblib')

    # Make predictions using the loaded model
    y_pred_IE = svm_model_IE.predict(my_X_tfidf)[0]
    y_pred_NS = svm_model_NS.predict(my_X_tfidf)[0]
    y_pred_FT = svm_model_FT.predict(my_X_tfidf)[0]
    y_pred_JP = svm_model_JP.predict(my_X_tfidf)[0]

    results=[y_pred_IE,y_pred_NS,y_pred_FT,y_pred_JP]
    
    return translate_back(results)


#print(final("hey"))

