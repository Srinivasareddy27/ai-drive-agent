import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, redirect, request, jsonify, session
from flask_cors import CORS
from drive_service import create_flow, get_drive_service, list_files, download_file
from rag_pipeline import build_index, retrieve

app = Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app)

# GLOBAL STORAGE
documents = []
file_names = []
index = None

# ROOT
@app.route("/")
def home():
    return "AI Drive Agent Running"

# CONNECT DRIVE
@app.route("/connect-drive")
def connect_drive():
    flow = create_flow()

    auth_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    session['state'] = state
    session['code_verifier'] = flow.code_verifier

    return redirect(auth_url)

# CALLBACK
@app.route("/oauth2callback")
def oauth_callback():
    flow = create_flow()

    flow.code_verifier = session.get('code_verifier')

    flow.fetch_token(
        authorization_response=request.url
    )

    credentials = flow.credentials
    service = get_drive_service(credentials)

    app.config["drive_service"] = service

    return "Google Drive connected successfully!"

# SELECT FOLDER
@app.route("/select-folder", methods=["POST"])
def select_folder():
    global documents, file_names, index

    folder_id = request.json.get("folder_id")
    service = app.config.get("drive_service")

    if not service:
        return jsonify({"error": "Drive not connected"}), 400

    files = list_files(service, folder_id)

    documents = []
    file_names = []

    for f in files:
        content = download_file(service, f["id"])
        if content:
            documents.append(content)
            file_names.append(f["name"])

    index = build_index(documents)

    return jsonify({"message": "Documents indexed successfully"})

# CHAT API
@app.route("/chat", methods=["POST"])
def chat():
    global index, documents, file_names

    query = request.json.get("query")

    if index is None:
        return jsonify({"error": "No documents indexed"}), 400

    results = retrieve(query, index, documents, file_names)

    context = " ".join([r["text"] for r in results])

    answer = generate_answer(query, context)

    return jsonify({
        "answer": answer,
        "sources": [r["file"] for r in results]
    })

# SIMPLE ANSWER GENERATOR
def generate_answer(query, context):
    if not context.strip():
        return "No relevant information found"

    sentences = context.split(".")

    relevant = []
    for s in sentences:
        if any(word.lower() in s.lower() for word in query.split()):
            relevant.append(s.strip())

    if relevant:
        return ". ".join(relevant[:3])

    return "Answer not found in documents"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)