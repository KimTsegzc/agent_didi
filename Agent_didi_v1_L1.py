"""
Project: Agent_didi
Purpose: AI agent Calling service from didiglobal.com
Author: KimtseGZC
Date: 16Feb2025
Version: 1.0
Layer: L0
--------------------------------
Statement of L1:
Maintains all phone UI via:
(1) [click] a position dictionary for icons
(2) Keyboard typing
(3) Snapshot of the screen
(4) Check info from the snapshot
(5) Locate new icons if necessary
--------------------------------
Layers explanation:
L0 - I/O interface layer
L1 - phone interaction layer
L2 - event handling layer
L3 - service calling layer
"""


import pygetwindow as gw
import pyautogui
import time
from pathlib import Path
import keyboard

import Agent_didi_v1_L0 as L0
import L0_baidu_AI as baidu
import L0_OpenAI as openai


def L1_regist_icons():
    global posi, p_from, p_home, p_office, p_to, p_top, p_first_select
    mid_dx = posi["width"] // 2
    third_dx = posi["width"] // 3
    p_from = nposi(mid_dx, 470)
    p_home = nposi(130, 210)
    p_office = nposi(350, 210)
    p_to = nposi(third_dx, 530)
    p_top = nposi(mid_dx, 110)
    p_first_select = nposi(mid_dx, 230)


def switch_n_shot(app_name, snapshot_filename="./media/snapshot.png"):
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


def L1_fillin_from(from_pos):
    click_at_coordinates(p_from)
    if from_pos in ['家', '家里']:
        click_at_coordinates(p_home)
    elif from_pos in ['公司', '办公室']:
        click_at_coordinates(p_office)
    else:
        click_at_coordinates(p_top)
        type_in_text(from_pos)
        click_at_coordinates(p_first_select)


def L1_fillin_to(to_pos):
    click_at_coordinates(p_to)
    if to_pos in ['家', '家里']:
        click_at_coordinates(p_home)
    elif to_pos in ['公司', '办公室']:
        click_at_coordinates(p_office)
    else:
        click_at_coordinates(p_top)
        type_in_text(to_pos)
        click_at_coordinates(p_first_select)


def L1_pmpt_parse_from_to(human_input):
    # 根据用户需求，解析出发地和目的地
    prompt = '用户需求是：' + human_input + '。'
    prompt += '\n请从需求里区分出发地和目的地，用from=, to=, 来表示。'
    prompt += '\n中间用|分开。'
    response = openai.L0_OpenAI_chat(prompt)
    print('[L1]>> AI response: ', response)
    from_pos = response.split('from=')[1].split('|')[0]
    to_pos = response.split('to=')[1].split('|')[0]
    print('[L1]>> parsing from_pos: ', from_pos)
    print('[L1]>> parsing to_pos: ', to_pos)
    return from_pos, to_pos


def L1_pmpt_parse_service():
    # 根据页面信息，解析出服务信息
    prompt = '这是一个打车软件，用户刚完成订单输入'
    prompt += '请先用一句话介绍目前选中服务，应答时间、价格、里程、行程时间'
    prompt += '然后依次介绍各类服务价格'
    prompt += '注意，各类价格精确到元即可，不用小数点后面的内容'
    prompt += '不要开头和结尾的问候性回答，精简一点'
    url = "./media/snapshot.png"
    switch_n_shot("滴滴")
    print('[L1]>> parsing service info...')
    response = openai.L0_OpenAI_VL(prompt, url).replace('*', '')
    return response


if __name__ == "__main__":
    human_input = L0.L0_STT_listening()
    from_pos, to_pos = L1_pmpt_parse_from_to(human_input)    

    posi = switch_n_shot("滴滴")
    L1_regist_icons()
    
    L1_fillin_from(from_pos)
    L1_fillin_to(to_pos)
    time.sleep(2)

    service = L1_pmpt_parse_service()
    print(service)
    L0.L0_TTS_speak(service)