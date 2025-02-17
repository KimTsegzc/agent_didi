"""
Project: Agent_didi
Purpose: AI agent Calling service from didiglobal.com
Author: KimtseGZC
Date: 16Feb2025
Version: 1.0
Layer: [L0]
--------------------------------
Statement of [L0]
offers I/O for human interaction, includes:
(1) AI capabilities - OpenAI
(2) AI capabilities - Baidu
(3) Mic
(4) Speaker
(5) LBS
--------------------------------
Layers explanation:
[L0] - I/O interface layer
[L1] - phone interaction layer
[L2] - event handling layer
[L3] - service calling layer
"""

from playsound import playsound
import speech_recognition as sr

import L0_baidu_AI as baidu
import L0_OpenAI as openai
import L0_gaode_LBS as gaode


def L0_TTS(text, filename, src="Baidu"):
    print("[L0]>> Converting text to audio")
    if src == "OpenAI":
        openai.L0_OpenAI_TTS(text, filename)
    elif src == "Baidu":
        baidu.L0_Baidu_TTS(text, filename)


def L0_TTS_speak(text, filename="./media/output.mp3"):
    L0_TTS(text, filename, src="Baidu")
    print("[L0]>> Playing audio")
    playsound(filename)


def L0_STT_listening(lng='zh-CN'):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 1000  
    recognizer.dynamic_energy_threshold = True  
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic)
            print("[L0]>> Listening...")
            audio = recognizer.listen(mic)
            print("[L0]>> Recognizing...")
            text = recognizer.recognize_google(audio, language=lng)
            print(f"[L0]>> Transcription: {text}")
            return text
    except sr.UnknownValueError:
        print("[L0]!! Google could not understand.")
    except sr.RequestError as e:
        print(f"[L0]!! Could not request from Google; {e}")
    except Exception as e:
        print(f"[L0]!! An error occurred: {e}")
    return None


if __name__ == "__main__":
    # human_input = L0_STT_listening()
    # ai_chat = openai.L0_OpenAI_chat(human_input)
    # print(f"[L0]>> AI response: {ai_chat}")
    # L0_TTS_speak(ai_chat)
    print(gaode.L0_LBS_L2A(113.323, 23.124))