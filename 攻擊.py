"""
遊戲規則，按下空白鍵，不斷點擊，鬆開就放開
按下S鍵，不斷點擊[上]與[下]按鍵
"""

import pyautogui
import keyboard
import time

def mouse_click_while_space_pressed():
    while True:
        if keyboard.is_pressed('space'):
            pyautogui.click()
            time.sleep(0.001)
        if keyboard.is_pressed('s'):
            pyautogui.press('left')
            pyautogui.press('right')
        else:
            print("No spacebar pressed")
            time.sleep(0.5)

mouse_click_while_space_pressed()
