import re

import nltk
from nltk.corpus import stopwords

def get_stop_words(lang:str="english"):
    nltk.download("stopwords")
    return set(stopwords.words(lang))
