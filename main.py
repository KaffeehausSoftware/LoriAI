# Lori Assistant v0.1.0

import os
import sys
import time
import pyaudio
import playsound
from gtts import gTTS
import openai
import speech_recognition as sp
import dearpygui.dearpygui as dpg

api_key = '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'
lang = 'en'

openai.api_key = api_key

dpg.create_context()

def get_audio():
    r = sp.Recognizer()
    with sp.Microphone() as src:
        audio = r.listen(src)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)

            if "Lori" in said:
                completion = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": said}])
                text = completion.choices[0].message.content
                speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
                speech.save("speech.mp3")
                playsound.playsound("speech.mp3")
            if "stop running self" in said:
                print("Goodbye!")
                sys.exit()

        except Exception:
            print("Exception")

    return said


with dpg.window(tag="Lori Voice Assistant"):
    dpg.add_text("Welcome to Lori.")
    dpg.add_text("To ask Lori a question, say Hey Lori followed by what you want to ask.")
    dpg.add_text("To close Lori, say Stop Running Self.")
    dpg.add_text("Lori is powered by OpenAi.")
    dpg.add_text("Created by Kaffeehaus Software.")


dpg.create_viewport(title='Lori', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Lori Voice Assistant", True)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    get_audio()


dpg.destroy_context()
sys.exit()