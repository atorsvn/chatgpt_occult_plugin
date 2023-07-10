import os
import json
import string
import pickle
import gensim.downloader as gensim_downloader
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseTermSimilarityMatrix, WordEmbeddingSimilarityIndex
import nltk
from nltk.corpus import stopwords

class TextClassifier:
    def __init__(self, da_pickle_rick, embedding="glove-wiki-gigaword-300"):
        nltk.download("stopwords")
        self.stop_words = stopwords.words("english")

        self.CLASS_DOCS = self.load_data('data/777.json')
        classes_tokens_list = [self._filter_text_to_token_list(text) for text in self.CLASS_DOCS]
        self.classes_dictionary = Dictionary(classes_tokens_list)
        classes_bow_list = [self.classes_dictionary.doc2bow(token_list) for token_list in classes_tokens_list]
        self.tfidf = TfidfModel(classes_bow_list)
        self.classes_tfidf_list = [self._preprocess_text(text) for text in self.CLASS_DOCS]
        
        with open('data/777.json', encoding='utf8') as json_file:
            self.DATA_777 = json.load(json_file)
            
        self.KEYS = self.DATA_777["keys"]
        
        if os.path.exists(da_pickle_rick):
            with open(da_pickle_rick, "rb") as file:
                self.termsim_matrix = pickle.load(file)
        else:
            embedding_model = gensim_downloader.load(embedding)
            termsim_index = WordEmbeddingSimilarityIndex(embedding_model)
            self.termsim_matrix = SparseTermSimilarityMatrix(termsim_index, self.classes_dictionary, self.tfidf)
            with open("data/termsim_matrix.pickle", "wb") as file:
                pickle.dump(self.termsim_matrix, file)

    @staticmethod
    def load_data(json_path):
        with open(json_path, encoding='utf8') as json_file:
            return json.load(json_file)["docs"]

    def _filter_text_to_token_list(self, text):
        return [token.translate(str.maketrans('', '', string.punctuation)) for token in text.lower().split() if token not in self.stop_words]

    def _preprocess_text(self, text):
        return self.tfidf[self.classes_dictionary.doc2bow(self._filter_text_to_token_list(text))]

    def classify_text(self, text):
        input_tfidf = self._preprocess_text(text)
        similarities = [(i, self.termsim_matrix.inner_product(input_tfidf, class_tfidf, normalized=(True, True))) for i, class_tfidf in enumerate(self.classes_tfidf_list)]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return self.KEYS[similarities[0][0]]