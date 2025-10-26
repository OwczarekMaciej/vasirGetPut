import requests
import base64
import json
from datetime import datetime

# thread_id = "thread_ekuTmn2RgHR0WKGaDF3EL92Z"
# assistant_id = "asst_8KgflVesqua8aN7u5VFZ5u5P"

def upload_audio_file(api_url, file_path):
    try:
        with open(file_path, 'rb') as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        now = datetime.now()

        payload = {
            "audioData": encoded_audio
            # "thread_id": thread_id,
            # "assistant_id": assistant_id,
            #"time":  now.strftime("%d/%m/%Y %H:%M:%S")
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            filename = response_data.get('body')
            print(f"File uploaded successfully. Response: {filename}")
            return filename
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
upload_audio_file("https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/test/upload", "output.wav")

