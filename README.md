# sentence_embedder

## Sentence to embedding API demo for plagiarism detection.
Currently tested on, and uses a pre-trained model ('paraphrase-multilingual-mpnet-base-v2') from huggingface. Most plagiarized sentences have cosine distance less than **0.1**. Most sentences that are about similar topics, but nonetheless non-plagiarized, had cosine distance of about **0.5** or more.

### Pre-requisites
* CUDA 10.2

### Requirements
* Pytorch 1.12.1
* sentence_transformers 2.2.2
* transformers 4.23.1
* scipy
* numpy
* scikit-learn
* flask

*The code may work on other versions of torch/transformers. The specified version are merely the latest tested versions.*

### Usage
Local server can be turned on `localhost:8000` by running `convert_database.py`. For local usage, plain flask server should work fine. 

Turn on: `python convert_database.py`. API could be sped up by using a different backend for the server such as gunicorn. In such case, you may use: `gunicorn --workers <NUM_OF_WORKERS> --bind 0.0.0.0:8000 convert_database:app`

The server has two endpoints for: 
1. Embedding sentences 

   address: `0.0.0.0:8000/process`  
   receives: `{"text": string}`, returns: `{"embedding": list}`

3. Comparing two sentences with each other 

   address: `0.0.0.0:8000/compare`  
   recieves: `{"text": string}`, returns: `{"distance": float}` (make sure to put a period after each sentence.)

### TODO

* Train/finetune a new model with proprietary data.
* Batch processing
* Establish clear cosine distance threshold based on real world data


