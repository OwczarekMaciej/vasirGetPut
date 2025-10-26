import os
import requests

# === KONFIGURACJA ===
# Ustaw zmienną środowiskową ELEVENLABS_API_KEY, np.:
# export ELEVENLABS_API_KEY="twój_klucz_api"
API_KEY = "sk_a1e7834a9503e2f6d53cfb5e8bf7422b774d8cc6a5f0930d"
if not API_KEY:
    raise ValueError("Brak klucza API! Ustaw zmienną środowiskową ELEVENLABS_API_KEY")

# ID głosu – możesz zmienić na dowolny z Twojego konta ElevenLabs
VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"
OUTPUT_PATH = "output.mp3"
CHUNK_SIZE = 1024

# Endpoint – poprawny dla aktualnego API
TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "Accept": "audio/mpeg",                 # Oczekujemy pliku audio
    "Content-Type": "application/json",     # Wysyłamy JSON
    "xi-api-key": API_KEY
}

def text_to_speech(text: str) -> str | None:
    """Konwertuje tekst na mowę i zapisuje do pliku MP3."""
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.8,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True,
        },
        "output_format": "mp3_44100_128"  # opcjonalnie: kontrola jakości wyjścia
    }

    print("⏳ Wysyłanie żądania do ElevenLabs API...")
    response = requests.post(TTS_URL, headers=headers, json=data, stream=True)

    if response.status_code == 200:
        with open(OUTPUT_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        print(f"✅ Audio zapisane jako: {OUTPUT_PATH}")
        return OUTPUT_PATH
    else:
        print(f"❌ Błąd {response.status_code}: {response.text}")
        return None


if __name__ == "__main__":
    print("=== ElevenLabs Text-to-Speech Test ===")
    text = input("Wpisz tekst, który chcesz przekonwertować na mowę: ").strip()
    if text:
        text_to_speech(text)
    else:
        print("⚠️ Nie podano tekstu – zakończono działanie.")
