import requests
import base64
import json
import os
from datetime import datetime

API_GATEWAY_URL = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/test/upload"
FILE_PATH = "output.wav"


def upload_audio_file(api_url, file_path, voice_settings=None):
    try:
        with open(file_path, "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

        now = datetime.now()
        time_str = now.strftime("%d/%m/%Y %H:%M:%S")

        payload = {
            "audio_data": encoded_audio,
            "time": time_str,
            #"assistant_id": "",
        }

        if voice_settings is not None:
            payload["voice_settings"] = voice_settings

        print(f"Wysyłanie pliku {os.path.basename(file_path)} do {api_url}...")
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            filename = response_data.get("filename")
            print(f"File uploaded successfully. Response: {filename}")
            return filename
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# if __name__ == "__main__":
#     upload_audio_file(API_GATEWAY_URL, FILE_PATH)
