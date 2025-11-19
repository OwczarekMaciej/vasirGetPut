import time
import threading
import os

import flet as ft

import recordAudio
import putAudio
import getAudio


API_URL_UPLOAD = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/test/upload"
API_URL_DOWNLOAD = "https://apzna1a8ci.execute-api.eu-north-1.amazonaws.com/test/"
LOCAL_RECORDING_FILENAME = "output.wav"
RESPONSE_AUDIO_FILENAME = "response_audio.mp3"


def main(page: ft.Page):
    page.title = "VASIR Voice Assistant"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    
    is_recording = False
    record_thread = None

    status_text = ft.Text(
        "Press Start to activate voice command",
        size=16,
    )
    loading_text = ft.Text(
        "",
        size=14,
        color="#888888",
    )

    # --- voice_id z UI ---
    voice_id_field = ft.TextField(
        label="ElevenLabs voice_id",
        value="Xb7hH8MSUJpSbSDYk0k2",  # domyślny / ulubiony głos
        width=400,
    )

    # --- labelki aktualnych wartości ---
    stability_value_text = ft.Text("0.50")
    similarity_value_text = ft.Text("0.80")
    style_value_text = ft.Text("0.00")

    # --- slidery ---
    def _update_slider_value(e: ft.ControlEvent, label: ft.Text):
        scaled = float(e.control.value) / 100.0
        label.value = f"{scaled:.2f}"
        page.update()

    stability_slider = ft.Slider(
        min=0,
        max=100,
        value=50,
        divisions=20,
        active_color="blue",
        on_change=lambda e: _update_slider_value(
            e, stability_value_text
        ),
    )
    similarity_slider = ft.Slider(
        min=0,
        max=100,
        value=80,
        divisions=20,
        active_color="blue",
        on_change=lambda e: _update_slider_value(
            e, similarity_value_text
        ),
    )
    style_slider = ft.Slider(
        min=0,
        max=100,
        value=0,
        divisions=20,
        active_color="blue",
        on_change=lambda e: _update_slider_value(
            e, style_value_text
        ),
    )
    speaker_boost_checkbox = ft.Checkbox(
        label="Use speaker boost",
        value=True,
    )

    # ustaw wartości początkowe labeli
    stability_value_text.value = f"{stability_slider.value / 100.0:.2f}"
    similarity_value_text.value = f"{similarity_slider.value / 100.0:.2f}"
    style_value_text.value = f"{style_slider.value / 100.0:.2f}"

    record_button = ft.ElevatedButton(
        "Start Recording",
        icon="🎙️",
        bgcolor="green",
        color="black",
    )

    stop_event = threading.Event()
    loading_flag = threading.Event()

    # --- zbieranie ustawień dla API ---

    def get_voice_settings():
        return {
            "stability": stability_slider.value / 100.0,
            "similarity_boost": similarity_slider.value / 100.0,
            "style": style_slider.value / 100.0,
            "use_speaker_boost": speaker_boost_checkbox.value,
        }

    def get_voice_id():
        return voice_id_field.value.strip()

    # --- audio workflow ---

    def record_audio_thread():
        recordAudio.record_audio(stop_event)

    def loading_animation():
        dots_cycle = ["", ".", "..", "..."]
        i = 0
        while loading_flag.is_set():
            loading_text.value = f"Processing{dots_cycle[i % len(dots_cycle)]}"
            i += 1
            page.update()
            time.sleep(0.3)
        loading_text.value = ""
        page.update()

    def poll_for_response_audio(response_filename: str):
        while True:
            try:
                audio_data = getAudio.get_audio_file(API_URL_DOWNLOAD, response_filename)
                if audio_data:
                    with open(RESPONSE_AUDIO_FILENAME, "wb") as f:
                        f.write(audio_data)

                    status_text.value = "✅ Response received. Playing audio..."
                    loading_flag.clear()
                    page.update()

                    os.system(f"afplay {RESPONSE_AUDIO_FILENAME}")
                    status_text.value = "Playback complete. Ready."
                    page.update()
                    break
                else:
                    status_text.value = "⏳ Waiting for response..."
                    page.update()
            except Exception as e:
                status_text.value = f"Error during retrieval: {e}"
                loading_flag.clear()
                page.update()
                break

            time.sleep(1)

    def upload_and_get_response():
        try:
            voice_settings = get_voice_settings()
            voice_id = get_voice_id()

            response_filename = putAudio.upload_audio_file(
                API_URL_UPLOAD,
                LOCAL_RECORDING_FILENAME,
                voice_settings=voice_settings,
                voice_id=voice_id,
            )
            if response_filename:
                status_text.value = "Uploaded. Waiting for response..."
                loading_flag.set()
                page.update()

                threading.Thread(target=loading_animation, daemon=True).start()
                threading.Thread(
                    target=poll_for_response_audio,
                    args=(response_filename,),
                    daemon=True,
                ).start()
            else:
                status_text.value = "Upload failed. Check connection."
                page.update()
        except Exception as e:
            status_text.value = f"Error: {e}"
            page.update()

    # --- handler przycisku ---

    def on_record_click(e):
        nonlocal is_recording, record_thread
        if not is_recording:
            stop_event.clear()
            is_recording = True
            status_text.value = "🔴 Recording... Say your command"
            record_button.text = "Stop Recording"
            record_button.bgcolor = "red"
            record_button.icon = "⏹️"
            page.update()

            record_thread = threading.Thread(
                target=record_audio_thread,
                daemon=True,
            )
            record_thread.start()
        else:
            stop_event.set()
            is_recording = False
            status_text.value = "Stopping recording..."
            page.update()

            if record_thread and record_thread.is_alive():
                record_thread.join()

            status_text.value = "Uploading audio..."
            record_button.text = "Start Recording"
            record_button.bgcolor = "green"
            record_button.icon = "🎙️"
            page.update()

            threading.Thread(
                target=upload_and_get_response,
                daemon=True,
            ).start()

    record_button.on_click = on_record_click

    # --- layout ---

    page.add(
        ft.Column(
            controls=[
                ft.Text("VASIR - Voice Assistant", size=26, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=record_button,
                    alignment=ft.alignment.center,
                    padding=10,
                ),
                status_text,
                loading_text,
                ft.Divider(),
                ft.Text("ElevenLabs", size=18, weight=ft.FontWeight.BOLD),
                voice_id_field,
                ft.Divider(),
                ft.Text("Voice settings", size=18, weight=ft.FontWeight.BOLD),

                ft.Row(
                    controls=[
                        ft.Text("Stability"),
                        stability_value_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                stability_slider,

                ft.Row(
                    controls=[
                        ft.Text("Similarity boost"),
                        similarity_value_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                similarity_slider,

                ft.Row(
                    controls=[
                        ft.Text("Style"),
                        style_value_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                style_slider,

                speaker_boost_checkbox,
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
