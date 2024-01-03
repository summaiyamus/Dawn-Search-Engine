import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess_content(content):
    # Convert to lowercase
    content = content.lower()

    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    text_content = soup.get_text()

    # Tokenize the text into individual words
    words = word_tokenize(text_content)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Remove punctuation and special characters
    words = [word for word in words if word.isalnum()]

    # Join the processed words into a string
    preprocessed_content = ' '.join(words)

    return preprocessed_content
