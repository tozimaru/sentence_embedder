# sentence_embedder

## Sentence to embedding API demo for plagiarism detection.
Currently tested on, and uses a pre-trained model ('paraphrase-multilingual-mpnet-base-v2') from huggingface. Most plagiarized sentences have cosine distance less than **0.3**. Exact matches have a positive value very close to **0**. Most sentences that are about similar topics, but nonetheless non-plagiarized, had cosine distance of about **0.5** or more.

### Pre-requisites
* CUDA 10.2

### Requirements
* Pytorch 1.12.1
* sentence_transformers 2.2.2
* transformers 4.23.1
* numpy
* FastAPI
* uvicorn

*The code may work on other versions of torch/transformers. The specified version are merely the latest tested versions.*

### DB requirement

- PostgreSQL 12 or higher
- [pgvector extension](https://github.com/pgvector/pgvector)

### Usage

Refer to `schema.sql` for database details. `.env` file should contain your db details.

To run the server:
`uvicorn document_embedder_api:app --host 0.0.0.0 --port 8000`

### API Endpoints

`POST /insert/`: Insert a document into the database. Each document should be a JSON object containing the content, title (optional), author (optional), written year (optional) and document type (required) of the document. For now the API splits the sentences jsut by `.`. This should be improved for future use.

Example request payload:

```json
{
    "content": "We present a neural network structure, ControlNet, to control pretrained large diffusion models to support additional input conditions. The ControlNet learns task-specific conditions in an end-to-end way, and the learning is robust even when the training dataset is small (< 50k)",
    "title": "Controlnet paper",
    "author": "Control N. Paper",
    "written_year": 2023,
    "document_type": "ai research"
}
```

`POST /search/`: Search for similar sentences. The request payload should include a list of sentences, the number of top-k results to return, and an optional cosine similarity threshold.

Example request payload:

```json
{
    "sentences": [
        "This is a test sentence."
    ],
    "k": 5,
    "threshold": 0.7
}
```
### Client
The client.py script demonstrates how to interact with the API server. The script inserts sample documents into the database and searches for similar sentences using the /search/ endpoint. 

### TODO

* Better sentence tokenizing technique.
* Create embedding index, something like: `CREATE INDEX ON sentences USING ivfflat (embedding vector_cosine_ops);`


