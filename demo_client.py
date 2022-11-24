import requests
import json

#send to embedder
data = {'text': 'hello there, young man.'}
resp = requests.post('http://0.0.0.0:8000/process', data=json.dumps(data), headers={'content-type': 'application/json'})
print(resp.text)

#send to comparer
data = {'text': 'hello there, young man. I am not a young man, young man.'}
resp = requests.post('http://0.0.0.0:8000/compare', data=json.dumps(data), headers={'content-type': 'application/json'})
print(resp.text)