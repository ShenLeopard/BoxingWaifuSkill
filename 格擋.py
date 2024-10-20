"""
遊戲規則，有上下左右四個區域
偵測每個區域是 黃色 或是 藍色 ..其他顏色不做動作
若是黃色: 按下相應區域的鍵
若是藍色: 按下相反區域的鍵
"""
import threading
import pyautogui
import cv2
import numpy as np
import time

# 定義區域座標
Ax1, Ay1, Ax2, Ay2 = 886, 266, 1035, 401   # (上畫面)
Bx1, By1, Bx2, By2 = 591, 513, 737, 648    # (左畫面)
Cx1, Cy1, Cx2, Cy2 = 1191, 513, 1337, 648  # (右畫面)
Dx1, Dy1, Dx2, Dy2 = 886, 751, 1035, 886   # (下畫面)

# 顏色定義
YELLOW_BGR = [236, 182, 0]  # 黃色
RED_BGR = [0, 0, 255]       # 紅色
BLUE_BGR = [0, 220, 236]    # 藍色
# 顏色匹配的像素數量閾值
MIN_PIXELS_MATCH = 5  # 至少匹配5個像素才算，意即，超過五個像素是這個顏色，就當作是此顏色

# 檢查區域內特定顏色像素的數量
def check_color_exact(region, target_bgr):
    # 建立與區域大小相同的顏色矩陣
    target_color_matrix = np.full(region.shape, target_bgr, dtype=np.uint8)
    # 檢查每個像素是否與目標顏色匹配
    match_matrix = np.all(region == target_color_matrix, axis=-1)
    # 計算匹配的像素數量
    matched_pixels = np.sum(match_matrix)
    return matched_pixels

# 顏色檢查並按鍵
def check_color(region, direction_key, reverse_key):
    yellow_pixels = check_color_exact(region, YELLOW_BGR)
    red_pixels = check_color_exact(region, RED_BGR)
    blue_pixels = check_color_exact(region, BLUE_BGR)

    # 檢查黃色
    if yellow_pixels >= MIN_PIXELS_MATCH:
        print(f"黃色被偵測，按{direction_key}")
        pyautogui.press(direction_key)
    # 檢查紅色
    elif red_pixels >= MIN_PIXELS_MATCH:
        print("紅色被偵測，無需動作")
    # 檢查藍色
    elif blue_pixels >= MIN_PIXELS_MATCH:
        print(f"藍色被偵測，按反方向鍵{reverse_key}")
        pyautogui.press(reverse_key)
    else:
        print("未偵測到目標顏色")

# 檢查四個區域的顏色
def check_A():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    region_A = screenshot_np[Ay1:Ay2, Ax1:Ax2]
    check_color(region_A, 'up', 'down')

def check_B():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    region_B = screenshot_np[By1:By2, Bx1:Bx2]
    check_color(region_B, 'left', 'right')

def check_C():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    region_C = screenshot_np[Cy1:Cy2, Cx1:Cx2]
    check_color(region_C, 'right', 'left')

def check_D():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    region_D = screenshot_np[Dy1:Dy2, Dx1:Dx2]
    check_color(region_D, 'down', 'up')

# 主函數
def main():
    while True:
        t1 = threading.Thread(target=check_A)
        t2 = threading.Thread(target=check_B)
        t3 = threading.Thread(target=check_C)
        t4 = threading.Thread(target=check_D)

        # 啟動執行緒
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # 等待所有執行緒完成
        t1.join()
        t2.join()
        t3.join()
        t4.join()

        print("所有執行緒已完成，進入下一個迴圈")


# 執行主函數
if __name__ == "__main__":
    main()
