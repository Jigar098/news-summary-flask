from flask import Flask ,request, jsonify
import requests
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import newspaper
import urllib.request

app = Flask(__name__)

@app.route('/',methods = ['GET'])
def index():
    dictionary = {}
    url = request.args['url']
    nltk.download('stopwords')
    nltk.download('punkt')
    article = newspaper.Article(url,language = 'en')
    article.download()
    article.parse()
    article.nlp()

    # Tokenizing the text 
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(article.text)

    # Creating a frequency table to keep the 
    # score of each word 
    freqTable = dict() 
    for word in words:
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Creating a dictionary to keep the score 
    # of each sentence 
    sentences = sent_tokenize(article.text)
    sentenceValue = dict()

    for sentence in sentences: 
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else:
                    sentenceValue[sentence] = freq 

    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 

    # Average value of a sentence from the original text 

    average = int(sumValues / len(sentenceValue)) 

    # Storing sentences into our summary. 
    summary = '' 
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence

    dictionary['article sumary'] = summary
    return jsonify(dictionary)

if __name__ == "__main__":
    app.run(debug=True)