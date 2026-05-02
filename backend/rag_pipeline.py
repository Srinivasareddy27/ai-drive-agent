from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

docs_store = []


def build_index(documents):
    global docs_store
    docs_store = documents

    embeddings = model.encode(documents)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index


def retrieve(query, index, docs_store, file_names, k=3):
    query_embedding = model.encode([query])

    D, I = index.search(query_embedding, k)

    results = []
    for i in I[0]:
        results.append({
            "text": docs_store[i],
            "file": file_names[i]
        })

    return results