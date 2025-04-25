from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

SOLR_BASE_URL = "http://localhost:8983/solr/abubakar_collection"

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")

        solr_response = requests.get(f"{SOLR_BASE_URL}/select", params={
            "q": f"title:{query}" if query else "*:*",
            "fl": "id,title,category,author,published",
            "rows": 10,
            "wt": "json"
        })

        solr_data = solr_response.json()
        if "response" in solr_data and "docs" in solr_data["response"]:
            results = solr_data["response"]["docs"]
        else:
            results = []

        return render_template("index.html", query=query, results=results)

    return render_template("index.html")

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")
    solr_response = requests.get(f"{SOLR_BASE_URL}/select", params={
        "q": f"title:{query}*",
        "fl": "title",  # Only return title field
        "rows": 10,  # Limit the number of suggestions
        "wt": "json"
    })

    solr_data = solr_response.json()
    if "response" in solr_data and "docs" in solr_data["response"]:
        suggestions = [{"title": doc["title"][0]} for doc in solr_data["response"]["docs"]]
    else:
        suggestions = []
    return jsonify(suggestions)

if __name__ == "__main__":
    app.run(debug=True)
