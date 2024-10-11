import requests
import base64

def send_audio_file(api_gateway_url, file_path, filename):
    try:
        with open(file_path, "rb") as audio_file:
            audio_binary = audio_file.read()
        
        audio_base64 = base64.b64encode(audio_binary).decode('utf-8')
        
        payload = {
            "filename": filename,
            "audio_data": audio_base64
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.put(api_gateway_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"Audio file '{filename}' uploaded successfully.")
        else:
            print(f"Failed to upload audio file. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
api_gateway_url = "https://dbf3jvpmx7.execute-api.eu-north-1.amazonaws.com/dev1/put"
file_path = "request_recording.wav"
filename = "example_audio.wav"
send_audio_file(api_gateway_url, file_path, filename)
