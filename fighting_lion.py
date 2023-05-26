import numpy as np
from PIL import ImageGrab
import time
import scipy.signal
import win32api, win32con, win32com.client
import keyboard

def knight(ref_img, x_start, y_start, x_end, y_end):
    knight_img = ImageGrab.grab(bbox=(x_start,y_start, x_end, y_end)).convert("L")
    knight_img =np.array(knight_img)
    knight_img = knight_img.astype(np.float64)
    knight_img -= np.mean(knight_img)
    corr_img = scipy.signal.fftconvolve(knight_img, ref_img[::-1,::-1], mode='same') # Convolve both images using Fast Fourier Transform
    shift = np.unravel_index(np.argmax(corr_img), corr_img.shape)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, shift[1] - 100, shift[0] - 100, 0, 0) # Move mouse in the opposite direction of the shift



if __name__ == "__main__":
    # EDIT THESE VALUES

    HORIZONTAL_RES = 2560
    VERTICAL_RES = 1440
    # 1416, 293
    x_start = int(1416 - 100)
    y_start = int(200  - 100)

    x_end = int(1416 + 100)
    y_end = int(200 + 100)
    # EDIT ABOVE THIS LINE
    
    keyboard.wait('g')

    ref_img_knight = ImageGrab.grab(bbox=(x_start,y_start, x_end, y_end)).convert("L")  # X1,Y1,X2,Y2
    #ref_img_knight.save("ref_img_knight.png")
    ref_img_knight = np.array(ref_img_knight)
    ref_img_knight = ref_img_knight.astype(np.float64)
    ref_img_knight -= np.mean(ref_img_knight)
    shell = win32com.client.Dispatch("WScript.Shell")
    
    
    
    # STEP 1 KILL KNIGHT
    # STEP 2 Detect glimmer drop
    # STEP 3 if glimmer drop, move mouse to symbol
    # STEP 4 shoot once
    # STEP 5 go back to step 1

    while True:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 516, 0, 0, 0)
        
        #Shoot Symbol
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -516, 0, 0, 0)
        time.sleep(0.3)

        i = 0
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        while (i < 10):
            time.sleep(0.2)
            knight(ref_img_knight, x_start, y_start, x_end, y_end)

            i += 1
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            
        time.sleep(1)
        knight(ref_img_knight, x_start, y_start, x_end, y_end)
        time.sleep(0.1)
        keyboard.press_and_release('r')
        time.sleep(1)
        keyboard.press_and_release('p')
        time.sleep(2)
        win32api.SetCursorPos((1120,614)) # finest matterweave
        time.sleep(0.1)
        keyboard.press('f')
        time.sleep(1.1)
        keyboard.release('f')
        time.sleep(0.1)
        keyboard.press_and_release('p')
        time.sleep(3)
