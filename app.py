import os
import json
import quart
import quart_cors
from quart import request
from text_classifier import TextClassifier
from gematria import GematriaCalculator
from text_similarity import TextSimilarity  # Assuming this is the file where your class is

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

classifier = TextClassifier('termsim_matrix.pickle')
calculator = GematriaCalculator()
similarity = TextSimilarity("sentence-transformers/all-MiniLM-L6-v2", "data/libri_corpus.json")

@app.post("/gematria")
async def calculate_gematria_route():
    request_data = await request.get_json(force=True)
    text = request_data.get('text', '')

    gematria_result = calculator.calculate_gematria(text)
    return quart.Response(response=json.dumps(gematria_result), status=200)

@app.post("/classify")
async def classify_text():
    request_data = await request.get_json(force=True)
    text = request_data.get('text', '')
    classification = classifier.classify_text(text)
    return quart.Response(response=json.dumps({"classification": classification}), status=200)

@app.post("/similarity")
async def get_similarity():
    request_data = await request.get_json(force=True)
    text = request_data.get('text', '')
    n_results = request_data.get('n_results', 2)
    similarity.search(text, n_results)
    return quart.Response(response=json.dumps({"message": "Similarity search completed"}), status=200)

@app.post("/all")
async def all_in_one():
    request_data = await request.get_json(force=True)
    text = request_data.get('text', '')
    n_results = request_data.get('n_results', 2)

    # Calculate Gematria
    gematria_result = calculator.calculate_gematria(text)

    # Classify Text
    classification = classifier.classify_text(text)

    # Get Similarity
    similarity_results = similarity.search(text, n_results)

    # Combine all results into one JSON response
    result = {
        "gematria": gematria_result,
        "classification": classification,
        "similarity": similarity_results
    }

    return quart.Response(response=json.dumps(result), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
