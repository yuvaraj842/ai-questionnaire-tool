from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Step 5 - Split text into chunks
def split_text(text, chunk_size=200):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks


# Step 6 - Load reference documents
def load_documents(folder="references"):

    docs = []

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:

            text = f.read()

            docs.append((file, text))

    return docs


# Step 6 - Build FAISS vector database
def build_vector_store():

    docs = load_documents()

    chunks = []
    sources = []

    for filename, text in docs:

        text_chunks = split_text(text)

        for chunk in text_chunks:

            chunks.append(chunk)
            sources.append(filename)

    embeddings = model.encode(chunks)

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, chunks, sources


# Step 7 - Retrieve relevant chunks
def retrieve_context(question, index, chunks, sources):

    q_embedding = model.encode([question])

    distances, indices = index.search(np.array(q_embedding), k=3)

    results = []

    for i in indices[0]:

        results.append((chunks[i], sources[i]))

    return results


# Step 8 - Generate answer using retrieved context
def generate_answer(question, retrieved_chunks):

    context_text = " ".join([c[0] for c in retrieved_chunks])

    citation = retrieved_chunks[0][1]

    if context_text.strip() == "":
        return "Not found in references.", "None"

    if question.lower() in context_text.lower():
        answer = context_text
    else:
        answer = context_text[:200]

    return answer, citation

# Step 9 - Full pipeline
def answer_question(question, index, chunks, sources):

    retrieved = retrieve_context(question, index, chunks, sources)

    answer, citation = generate_answer(question, retrieved)

    return answer, citation, retrieved