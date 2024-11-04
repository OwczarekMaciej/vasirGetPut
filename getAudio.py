import requests
import base64
import json

def get_audio_file(api_gateway_url, filename):
    try:
        url = f"{api_gateway_url}?filename={filename}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            audio_base64 = data.get("audio_data")
            if audio_base64:
                audio_binary = base64.b64decode(audio_base64)
                
                with open(filename, "wb") as audio_file:
                    audio_file.write(audio_binary)
                
                print(f"Audio file '{filename}' downloaded and saved successfully.")
            else:
                print("No audio data found in the response.")
        else:
            print(f"Failed to retrieve audio file. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

api_gateway_url = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/dev"
filename = "1730761121.mp3"
get_audio_file(api_gateway_url, filename)
