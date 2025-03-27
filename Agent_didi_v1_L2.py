"""
Project: Agent_didi
Purpose: AI agent Calling service from didiglobal.com
Author: KimtseGZC
Date: 16Feb2025
Version: 1.0
Layer: L0
--------------------------------
Statement of L2:
Packed chain of event(CoE):
(1) back to home
(2) config location
(3) config destination
(4) selection from places
(5) selection from services
--------------------------------
Layers explanation:
L0 - I/O interface layer
L1 - phone interaction layer
L2 - event handling layer
L3 - service calling layer
"""


from openai import OpenAI
from gtts import gTTS
from playsound import playsound
import pygetwindow as gw
import speech_recognition as sr
import pyautogui
import time
from pathlib import Path
import keyboard
import base64
import os

from L0_OpenAI import L0_OpenAI_VL, L0_OpenAI_TTS, L0_OpenAI_chat

def switch_to_app_and_snapshot(app_name, snapshot_filename="snapshot.png"):
    # Find the window with the specified name
    windows = gw.getWindowsWithTitle(app_name)
    if windows:
        app_window = windows[0]
        # Activate the window
        app_window.activate()
        time.sleep(1)
        # Take a screenshot of the window
        screenshot = pyautogui.screenshot(region=(
            app_window.left,
            app_window.top,
            app_window.width,
            app_window.height
        ))
        # Save the screenshot
        screenshot.save(snapshot_filename)
        print(f"Snapshot saved as {snapshot_filename}")
        return {
            "x": app_window.left,
            "y": app_window.top,
            "width": app_window.width,
            "height": app_window.height
        }
    else:
        print(f"No window found with title containing '{app_name}'")


def listen_and_transcribe():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Microphone initialized.")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language='zh-CN')
            print(f"Transcription: {text}")
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None
    

def init():
    global client
    key = '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'
    client = OpenAI(api_key=key)


def click_at_coordinates(p):
    pyautogui.click(p['x'], p['y'])
    print(f"Clicked at ({p['x']}, {p['y']})")
    time.sleep(1)


def type_in_text(text):
    keyboard.write(text)
    print(f"Typed text: {text}")
    time.sleep(1)


def nposi(dx, dy):
    return {"x": posi["x"] + dx, "y": posi["y"] + dy}


def call_service(from_pos, to_pos):
    mid_dx = posi["width"] // 2
    third_dx = posi["width"] // 3
    p_from = nposi(mid_dx, 470)
    p_to = nposi(third_dx, 530)
    p_top = nposi(mid_dx, 110)
    p_first_select = nposi(mid_dx, 230)
    p_home = nposi(130, 210)
    p_back = nposi(30, 56)
    if "家" in from_pos:
        click_at_coordinates(p_from)
    click_at_coordinates(p_home)
    click_at_coordinates(p_to)
    click_at_coordinates(p_top)
    type_in_text(to_pos)
    click_at_coordinates(p_first_select)
    time.sleep(2)

if __name__ == "__main__":
    init()
    human_input = listen_and_transcribe()
    # human_input = '从家里打车去天德广场'
    posi = switch_to_app_and_snapshot("滴滴")
    prompt = '这是一句用户从出发地到目的地的描述，请提取出出发地和目的地'
    prompt += '注意严格按照出发地=，目的地='
    prompt += '单行单句，不要有问候性回答，用户的描述是：'
    prompt += human_input

    response = L0_OpenAI_chat(prompt)
    print(response)
    call_service('家', '天德广场')

    prompt = '这是一个打车软件，用户刚完成订单输入'
    prompt += '请先用一句话介绍目前选中服务，应答时间、价格、里程、行程时间'
    prompt += '然后依次介绍各类服务价格'
    prompt += '注意，各类价格精确到元即可，不用小数点后面的内容'
    prompt += '不要开头和结尾的问候性回答，精简一点'
    url = "./snapshot.png"
    switch_to_app_and_snapshot("滴滴")
    response = L0_OpenAI_VL(prompt, url).replace('*', '')
    print(response)
    L0_OpenAI_TTS(response)
    playsound('./media/output.mp3')