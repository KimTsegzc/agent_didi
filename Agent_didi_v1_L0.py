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
(1) tts
(2) stt
(3) AI capabilities - openAI
(4) AI capabilities - Baidu
--------------------------------
Layers explanation:
[L0] - I/O interface layer
[L1] - phone interaction layer
[L2] - event handling layer
[L3] - service calling layer
"""


import openai
from openai import OpenAI
from playsound import playsound
import speech_recognition as sr
from pathlib import Path
import L0_baidu_AI as baidu
import base64
import os


def L0_OpenAI_chat(prompt):
    if O_source == "OpenAI" or O_source == "Nuwa":
        model = "gpt-4o"
    elif O_source == "Kimi":
        model = "moonshot-v1-32k"
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def L0_OpenAI_VL(prompt, url):
    if O_source == "OpenAI" or O_source == "Nuwa":
        model = "gpt-4o-mini"
    elif O_source == "Kimi":
        model = "moonshot-v1-8k-vision-preview"
    base64_image = encode_image(url)
    chat = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return chat.choices[0].message.content


def L0_TTS(text, filename, src="Baidu"):
    print("[L0]>> Converting text to audio")
    speech_file_path = Path(__file__).parent / filename
    if src == "OpenAI":
        with client.audio.speech.with_streaming_chat.create(
            model="tts-1",
            voice="alloy",
            input=text,
            speed=1.3,
        ) as chat:
            chat.stream_to_file(speech_file_path)
    elif src == "Baidu":
        baidu.L0_Baidu_TTS(text, filename)


def L0_TTS_speak(text, filename="./media/output.mp3"):
    L0_TTS(text, filename, src="Baidu")
    print("[L0]>> Playing audio")
    playsound(filename)


def L0_STT_listening(lng='zh-CN'):
    recognizer = sr.Recognizer()
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


def init(src):
    global client
    global O_source, key, url
    O_source = src
    if O_source == "OpenAI":
        url = "https://api.openai.com/v1"
        key = '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'
    elif O_source == "Kimi":
        url = "https://api.moonshot.cn/v1"
        key = 'sk-FTuSJsDw564gcsMHjUN0RaDBo3n6S8Qs2JVw23mZlCJnTqVW'
    elif O_source == "Nuwa":
        url = "https://api.nuwaapi.com/v1"
        key = 'sk-oxirYGNoyv0otJJZiIS6iB9zdmyjVr3KbKdd5WTQMQfsYjr8'
    else:
        raise ValueError(f"Unknown O_source: {O_source}")
    client = OpenAI(
        api_key=key,
        base_url=url,
    )
    # -----------Baidu API info-----------
    API_KEY = 'syWLArnalaUQEGzh8YawpjMP'
    SECRET_KEY = 'R6pjTuDkyO2t5RDwodvgo48L8cRY7HJM'
 

if __name__ == "__main__":
    init("Kimi")
    human_input = L0_STT_listening()
    ai_chat = L0_OpenAI_chat(human_input)
    print(f"[L0]>> AI response: {ai_chat}")
    L0_TTS_speak(ai_chat)