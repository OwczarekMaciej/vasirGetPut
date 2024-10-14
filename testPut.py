import requests
import base64
import json

api_url = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/dev/upload"

pdf_file_path = 'testFile.mp3'

with open(pdf_file_path, 'rb') as pdf_file:
    encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

payload = {
    "audioData": encoded_pdf
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(api_url, json=payload, headers=headers)

if response.status_code == 200:
    response_data = response.json()
    filename = response_data.get('body')
    print(filename)
    
else:
    print(f'Failed to upload file. Status code: {response.status_code}')
    print(response.text)
