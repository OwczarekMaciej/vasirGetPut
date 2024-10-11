import requests
import base64

def send_audio_file(api_gateway_url, file_path):
    try:
        # Read the audio file in binary mode
        with open(file_path, "rb") as audio_file:
            audio_binary = audio_file.read()
        
        # Convert audio to base64
        audio_base64 = base64.b64encode(audio_binary).decode('utf-8')
        
        # Prepare the payload
        payload = {
            "audioData": audio_base64
        }
        
        # Send the PUT request
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.put(api_gateway_url, json=payload, headers=headers)
        
        # Check the response
        if response.status_code == 200:
            print("Audio file uploaded successfully.")
        else:
            print(f"Failed to upload audio file. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
api_gateway_url = "https://dbf3jvpmx7.execute-api.eu-north-1.amazonaws.com/dev1/put"
file_path = "request_recording.wav"
send_audio_file(api_gateway_url, file_path)
