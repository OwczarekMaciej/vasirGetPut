import requests
import base64

def get_audio_file(api_gateway_url, filename):
    try:
        url = f"{api_gateway_url}?filename={filename}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            audio_base64 = data.get("audio_data")
            if audio_base64:
                return base64.b64decode(audio_base64)
            else:
                print("No audio data found in the response.")
                return None
        else:
            print(f"Failed to retrieve audio file. Status code: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
