import pyaudio
import wave
import threading
import testPut

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
filename = "output.wav"

stop_recording = False

def stop_recording_input():
    global stop_recording
    input("Press Enter to stop recording...\n")
    stop_recording = True

p = pyaudio.PyAudio()
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []

input_thread = threading.Thread(target=stop_recording_input)
input_thread.start()

print('Recording...')

while not stop_recording:
    data = stream.read(chunk)
    frames.append(data)

input_thread.join()

stream.stop_stream()
stream.close()
p.terminate()

print('Finished recording')

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

print(f"Recording saved as {filename}")
api_url = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/dev/upload"
testPut.upload_audio_file(api_url, filename)
