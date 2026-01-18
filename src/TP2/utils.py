import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download("stopwords")
nltk.download('wordnet')

def get_stop_words(lang:str="english"):
    return set(stopwords.words(lang))

STOPWORDS = get_stop_words()

def tokenize_text(text:str, normalize:bool=False) -> str:
    
    """A word split tokenizer"""
    
    text = text.lower()
    # on supprime la ponctuation
    text  = re.sub(r"[^\w\s]", "", text)
    # Tokenisation par espace
    tokens = text.split()
    # On ignore les stops words
    tokens = [t for t in tokens if t not in STOPWORDS]
    
    # On normalise le text si demandé
    if normalize:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
    
    return tokens
