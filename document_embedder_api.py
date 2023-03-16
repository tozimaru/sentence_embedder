from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

from utils import Document, Query

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

app = FastAPI()

@app.post("/documents/")
def add_document(document: Document):
    with engine.connect() as conn:
        result = conn.execute(text("INSERT INTO documents (content, title, author, written_year, document_type) VALUES (:content, :title, :author, :written_year, :document_type) RETURNING id"), 
        {"content": document.content, "title": document.title, "author": document.author, "written_year": document.written_year, "document_type": document.document_type})
        document_id = result.fetchone()[0]

        sentences = document.content.split(".")
        embeddings = model.encode(sentences)
        
        for position, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
            conn.execute(text("INSERT INTO sentences (document_id, content, embedding, position) VALUES (:document_id, :content, :embedding, :position)"),
                         {"document_id": document_id, "content": sentence, "embedding": str(embedding.tolist()), "position": position})

    return {"id": document_id}

@app.post("/search_id_only/")
def search_similar_sentences(query: Query):
    embeddings = model.encode(query.sentences)
    results = []

    with engine.connect() as conn:
        for sentence, embedding in zip(query.sentences, embeddings):
            search_params = {"k": query.k, "embedding": str(embedding.tolist())}
            search_query = "SELECT document_id, position, content, (embedding <=> vector(:embedding)) as distance FROM sentences"

            if query.threshold is not None:
                search_query += " WHERE (embedding <=> vector(:embedding)) <= :threshold"
                search_params["threshold"] = query.threshold

            search_query += " ORDER BY (embedding <=> vector(:embedding)) ASC LIMIT :k"

            result = conn.execute(text(search_query), search_params)
            similar_sentences = [{"document_id": row["document_id"], "position": row["position"], "content": row["content"], "distance": row["distance"]} for row in result]

            results.append({"input_sentence": sentence, "similar_sentences": similar_sentences})

    return results

@app.post("/search/")
def search_similar_sentences_meta(query: Query):
    embeddings = model.encode(query.sentences)
    results = []

    with engine.connect() as conn:
        for sentence, embedding in zip(query.sentences, embeddings):
            search_params = {"k": query.k, "embedding": str(embedding.tolist())}
            search_query = (
                "SELECT d.id, d.title, d.author, d.written_year, d.document_type, "
                "s.document_id, s.position, s.content, (s.embedding <=> vector(:embedding)) as distance "
                "FROM sentences s "
                "JOIN documents d ON s.document_id = d.id"
            )

            if query.threshold is not None:
                search_query += " WHERE (s.embedding <=> vector(:embedding)) <= :threshold"
                search_params["threshold"] = query.threshold

            search_query += " ORDER BY (s.embedding <=> vector(:embedding)) ASC LIMIT :k"

            result = conn.execute(text(search_query), search_params)
            similar_sentences = [
                {
                    "document_id": row["id"],
                    "title": row["title"],
                    "author": row["author"],
                    "written_year": row["written_year"],
                    "document_type": row["document_type"],
                    "position": row["position"],
                    "content": row["content"],
                    "distance": row["distance"],
                }
                for row in result
            ]

            results.append({"input_sentence": sentence, "similar_sentences": similar_sentences})

    return results