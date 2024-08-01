import os
import re
import string
from sklearn.feature_extraction.text import CountVectorizer

def load_files(dirs):
    documents = []
    labels = []
    for dir in dirs:
        for filename in os.listdir(dir):
            if filename.endswith('.txt'):
                with open(os.path.join(dir, filename), 'r', encoding='utf-8') as file:
                    documents.append(file.read())
                    labels.append(dir)
    return documents, labels

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def doc2set(text):
    cv = CountVectorizer(stop_words='english', binary=True)
    X = cv.fit_transform(text)
    doc = [set(doc.nonzero()[1]) for doc in X]
    return doc 

def idx2filename(idx, file_labels):
    return file_labels[idx]

class Document:
    def __init__(self, document:set, name:str):
        self.document = document
        self.name = name

def read_docs(dirs):
    documents, labels = load_files(dirs)
    clean_documents = [preprocess_text(document) for document in documents]
    documents = doc2set(clean_documents)
    documents = [Document(doc, name) for doc, name in zip(documents, labels)]
    return documents