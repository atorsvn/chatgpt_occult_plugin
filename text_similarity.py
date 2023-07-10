from txtai.embeddings import Embeddings
import json

class TextSimilarity:
    def __init__(self, path_to_embeddings, path_to_corpus):
        self.embeddings = Embeddings({"path": path_to_embeddings})
        self.data = self.load_corpus(path_to_corpus)
        self.index_corpus()

    def load_corpus(self, path_to_corpus):
        with open(path_to_corpus, "r") as f:
            data = json.load(f)
        return data

    def index_corpus(self):
        txtai_data = [(i, text["verse"], None) for i, text in enumerate(self.data)]
        self.embeddings.index(txtai_data)

    def search(self, query, n_results):
        results = self.embeddings.search(query, n_results)
        similarity_results = []
        for r in results:
            similarity_results.append({
                "text": self.data[r[0]]['label'] + " - " + self.data[r[0]]['verse'],
                "similarity": r[1]
            })
        return similarity_results
