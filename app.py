from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

SOLR_BASE_URL = "http://localhost:8983/solr/abubakar_collection"

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")

        solr_query = f"title:{query} OR category:{query} OR author:{query}" if query else "*:*"

        solr_response = requests.get(f"{SOLR_BASE_URL}/select", params={
            "q": solr_query,
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
    query = request.args.get("query", "").strip().lower()
    solr_query = f"title:{query}* OR category:{query}* OR author:{query}*" if query else "*:*"

    solr_response = requests.get(f"{SOLR_BASE_URL}/select", params={
        "q": solr_query,
        "fl": "title,category,author",
        "rows": 10,
        "wt": "json"
    })

    solr_data = solr_response.json()
    suggestions = set()  

    if "response" in solr_data and "docs" in solr_data["response"]:
        for doc in solr_data["response"]["docs"]:
            fields = []
            if "title" in doc:
                fields.extend(doc["title"])
            if "category" in doc:
                fields.extend(doc["category"])
            if "author" in doc:
                fields.extend(doc["author"])
            
            for field in fields:
                if query in field.lower():  
                    suggestions.add(field)

    return jsonify([{"value": suggestion} for suggestion in suggestions])

if __name__ == "__main__":
    app.run(debug=True)
