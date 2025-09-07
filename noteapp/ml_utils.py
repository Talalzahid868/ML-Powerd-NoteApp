from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.corpus import stopwords
from rake_nltk import Rake
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import pickle,os

# Rules Based Approach
# def auto_tag(text):
#     categories={
#         'Work':['meeting','project','deadline','client','report','presentation'],
#         'Personal':['family','friend','party','holiday','travel','hobby'],
#         'study':['exam','assignment','lecture','course','research','paper'],
#         'health':['doctor','exercise','diet','medication','appointment','wellness']
#         }
    
#     text = text.lower() 
#     for key, value_list in categories.items():
#         for word in value_list:
#             if word in text:
#                 return key
#     return "General"

# Ml-Based Auto Categorization
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)


category_map = {
    0: "Politics",
    1: "Sport",
    2: "Technology",
    3: "Entertainment",
    4: "Business"
}

def auto_tag(text):
    pred=model.predict([text])
    return category_map.get(pred[0],"General")

   
    



def extract_keywords(text):
    r=Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()[:5]

def generate_summary(text):
    parser=PlaintextParser.from_string(text,Tokenizer("english"))
    summarizer=LsaSummarizer()
    summary=summarizer(parser.document,1)
    return ' '.join([str(sentence) for sentence in summary])











