import requests
import json

# Replace the URL with the appropriate host and port where your API is running
API_URL = "http://localhost:8000"

def add_document(document):
    response = requests.post(f"{API_URL}/documents/", json=document)
    return response.json()

def search_similar_sentences(sentences, k=5, threshold=None):
    query = {"sentences": sentences, "k": k, "threshold": threshold}
    response = requests.post(f"{API_URL}/search/", json=query)
    return response.json()

if __name__ == "__main__":
    # example to add a new document
    doc = "We present a neural network structure, ControlNet, to control pretrained large diffusion models to support additional input conditions. The ControlNet learns task-specific conditions in an end-to-end way, and the learning is robust even when the training dataset is small (< 50k). Moreover, training a ControlNet is as fast as fine-tuning a diffusion model, and the model can be trained on a personal devices. Alternatively, if powerful computation clusters are available, the model can scale to large amounts (millions to billions) of data. We report that large diffusion models like Stable Diffusion can be augmented with ControlNets to enable conditional inputs like edge maps, segmentation maps, keypoints, etc. This may enrich the methods to control large diffusion models and further facilitate related applications."
    title = "ControlNet paper"
    author = "Control N. Paper"
    written_year = 2023
    document_type = "ai research"
    document = {"content": doc, "title": title, "author": author, "document_type": document_type, "written_year": written_year}
    added_document = add_document(document)
    print(f"Added document: {added_document}")

    # example to search for sentences
    search_sentences = ["The model learns task-specific conditions in an end-to-end way, and the learning is robust even when the training dataset is small", "today we went out"]
    search_results = search_similar_sentences(search_sentences, k=3, threshold=0.8)
    print(f"Search results: {json.dumps(search_results, indent=2)}")
