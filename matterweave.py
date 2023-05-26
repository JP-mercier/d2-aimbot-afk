import numpy as np
from PIL import Image, ImageGrab
import time
import keyboard
import scipy.signal
import win32api
import win32con
import win32com.client

# EDIT THESE VALUES
HORIZONTAL_RES = 2560
VERTICAL_RES = 1440
Trigger_coordinate = (168, 55)
# EDIT ABOVE THIS LINE

x_start = int(1950 - 100)
y_start = int(703 - 100)

x_end = int(1950 + 100)
y_end = int(703 + 100)

# Keybind for the trigger
keyboard.wait("g")
win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
time.sleep(.3)
ref_img = ImageGrab.grab(
    bbox=(x_start, y_start, x_end, y_end)).convert("L")  # X1,Y1,X2,Y2
#ref_img = ref_img.save("ref_img.png")
ref_img = np.array(ref_img)
ref_img = ref_img.astype(np.float64)
ref_img -= np.mean(ref_img)
shell = win32com.client.Dispatch("WScript.Shell")
while True:
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    # # Step 1: Loop until trigger (Radar detected)
    # trig_img = ImageGrab.grab(
    #     bbox=(0, 0, Trigger_coordinate[0] + 1, Trigger_coordinate[1] + 1))  # X1,Y1,X2,Y2
    # while (not (trig_img.getpixel(Trigger_coordinate)[0] > 50 and trig_img.getpixel(Trigger_coordinate)[1] < 80 and trig_img.getpixel(Trigger_coordinate)[2] < 50)):
    #     trig_img = ImageGrab.grab()
    #         bbox=(0, 0, Trigger_coordinate[0] + 1, Trigger_coordinate[1] + 1))  # X1,Y1,X2,Y2
    # Step 2: Shoot
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(.01)
    shell.SendKeys("a")
    shell.SendKeys("d")
    # Step 3: wait for shit to calm down
    time.sleep(3.7)  # Sleep for 3 seconds;ad
    bbox=(x_start, y_start, x_end, y_end).convert("L")
    #ref_img1 = ref_img1.save("ref_img1.png")
    ref_img1 = np.array(ref_img1)
    ref_img1 = ref_img1.astype(np.float64)
    ref_img1 -= np.mean(ref_img1)

    # Convolve both images using Fast Fourier Transform
    corr_img = scipy.signal.fftconvolve(
        ref_img1, ref_img[::-1, ::-1], mode='same')
    # corr_img *= (255.0/corr_img.max()) # Normalization to 0-255 (Only if you want to display the convolved image)
    #data = Image.fromarray(corr_img)
    # data.show()
    print(np.unravel_index(np.argmax(corr_img), corr_img.shape))
    # The brightest pixel /largest value is the "real center",
    shift = np.unravel_index(np.argmax(corr_img), corr_img.shape)
    # the difference between the coordinate of the "real center" and [100,100], which is the "true center", is the shift
    # Move mouse in the opposite direction of the shift
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,
                         shift[1] - 100, shift[0] - 100, 0, 0)
    time.sleep(0.625)
