from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from langdetect import detect 

def is_english(text):
    """Check if the input text is in English."""
    try:
        return detect(text) == "en" 
    except:
        return False

def preprocess_text(text):
    """Preprocess the given text by tokenizing, removing stopwords, and lemmatizing."""
    if isinstance(text, str):
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
        return ' '.join(lemmatized_tokens)
    return ""
