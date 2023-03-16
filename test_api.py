import json
from fastapi.testclient import TestClient
from document_embedder_api import app

client = TestClient(app)

def test_insert_document():
    document = {
        "title": "Test Document",
        "content": "This is a sample document. This is the second sentence",
        "author": "Lambo",
        "year": 2011,
        "document_type": "Test Article",
    }

    response = client.post("/documents/", json=document)
    assert response.status_code == 200

def test_search_similar_sentences():
    query = {
        "sentences": ["This is a test sentence."],
        "k": 5,
        "threshold": 0.7,
    }

    response = client.post("/search/", json=query)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["input_sentence"] == query["sentences"][0]
    assert len(data[0]["similar_sentences"]) > 0

def test_search_similar_sentences_no_threshold():
    query = {
        "sentences": ["This is a test sentence."],
        "k": 5,
    }

    response = client.post("/search/", json=query)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["input_sentence"] == query["sentences"][0]
    assert len(data[0]["similar_sentences"]) > 0


