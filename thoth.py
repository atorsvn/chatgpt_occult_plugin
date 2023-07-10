from gensim import corpora, models, similarities
import json
import random

class TarotReading:

    def __init__(self, tarot_file):
        self.tarot_file = tarot_file
        self.load_cards()
        self.prepare_similarity_search()

    def load_cards(self):
        with open(self.tarot_file, 'r', encoding='utf-8') as f:
            self.cards = json.load(f)

    def draw_cards(self, num_cards=3):
        return random.sample(self.cards, num_cards)

    def read_cards(self, cards):
        reading = []
        for card in cards:
            reading.append({
                'name': card['name'],
                'interpretation': card['interpretation'],
                'attributes': card['attributes']
            })
        return reading

    def three_card_reading(self):
        drawn_cards = self.draw_cards()
        return self.read_cards(drawn_cards)

    def prepare_similarity_search(self):
        self.indexes = {}
        self.dictionaries = {}
        self.corpus_tfidfs = {}
        self.tfidfs = {}

        for field in ['name', 'interpretation', 'attributes']:
            texts = [[word for word in document[field].lower().split()] for document in self.cards]
            self.dictionaries[field] = corpora.Dictionary(texts)
            corpus = [self.dictionaries[field].doc2bow(text) for text in texts]
            self.tfidfs[field] = models.TfidfModel(corpus)
            self.corpus_tfidfs[field] = self.tfidfs[field][corpus]
            self.indexes[field] = similarities.SparseMatrixSimilarity(self.corpus_tfidfs[field], num_features=len(self.dictionaries[field]))

    def search_by_name(self, query):
        return self.search_card(query, 'name')

    def search_by_interpretation(self, query):
        return self.search_card(query, 'interpretation')

    def search_by_attributes(self, query):
        return self.search_card(query, 'attributes')

    def search_card(self, query, field):
        vec_bow = self.dictionaries[field].doc2bow(query.lower().split())
        vec_tfidf = self.tfidfs[field][vec_bow]
        sims = self.indexes[field][vec_tfidf]
        best_match_index = sims.argmax()
        return self.cards[best_match_index]

    def search_all_fields(self, query):
        results = {}
        for field in ['name', 'interpretation', 'attributes']:
            result = self.search_card(query, field)
            results[field] = result
        return results

tarot = TarotReading("data/thoth.json")

# Search by card name
search_result_by_name = tarot.search_by_name("The Magus")
print("Search result by name: ", search_result_by_name)

# Search by card interpretation
search_result_by_interpretation = tarot.search_by_interpretation("beginnings freedom")
print("Search result by interpretation: ", search_result_by_interpretation)

# Search by card attributes
search_result_by_attributes = tarot.search_by_attributes("Capricorn")
print("Search result by attributes: ", search_result_by_attributes)

# Search by all fields
search_result_all = tarot.search_all_fields("innocence")
print("Search result all fields: ", search_result_all)
