import requests
import base64

thread_id = "thread_ekuTmn2RgHR0WKGaDF3EL92Z"
assistant_id = "asst_1PoJ2H6emUlIq0zgzp9OFaid"

def send_audio_file(api_gateway_url, file_path):
    try:

        with open(file_path, "rb") as audio_file:
            audio_binary = audio_file.read()
        
        audio_base64 = base64.b64encode(audio_binary).decode('utf-8')
        #print(audio_base64)

        payload = {
            "audioData": audio_base64,
            "thread_id": thread_id,
            "assistant_id": assistant_id
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(api_gateway_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("Audio file uploaded successfully.")
        else:
            print(f"Failed to upload audio file. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
api_gateway_url = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/dev/upload"
#api_gateway_url = 'https://2t5njgv827.execute-api.eu-north-1.amazonaws.com/devTest/upload'
file_path = "testFile.mp3"
send_audio_file(api_gateway_url, file_path)
