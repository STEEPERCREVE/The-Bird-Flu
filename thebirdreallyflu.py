#ATTEMPT TWO
import tkinter as tk
import random
import threading
import os
import sys
from playsound import playsound
from PIL import Image, ImageTk
import ctypes
import platform

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def play():
    def sound_thread():
        isitepic = random.randrange(0, 1_000)
        if isitepic != 1000:
            sound_list = [
                'tweet.mp3', 'chirp.mp3', 'caw.mp3', 'chichi.mp3',
                'woot.mp3', 'birdsound.wav', 'meow.wav', 'whowho.wav', 'whistle.mp3'
            ]
            sound = random.choice(sound_list)
        else:
            sound = 'ultra rare sound!.wav'

        playsound(resource_path(sound))  # ✅ Uses resource_path

    threading.Thread(target=sound_thread, daemon=True).start()

def makebird():
    win = tk.Toplevel()
    
    dx = random.choice([-5, 5])
    dy = random.choice([-5, 5])

    start_x = random.randint(100, 1000)
    start_y = random.randint(100, 600)
    win.geometry(f"+{start_x}+{start_y}")

    def move_window():
        nonlocal dx, dy
        x = win.winfo_x()
        y = win.winfo_y()
        new_x = x + dx
        new_y = y + dy

        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        win_width = win.winfo_width()
        win_height = win.winfo_height()

        bounced = False

        # Check if the bird is at the X edge and adjust direction gradually
        if new_x + win_width >= screen_width or new_x <= 0:
            if dx == 0: 
                dx = random.choice([-5, 5])  # Prevent being stuck by ensuring movement
            else:
                # Gradually change the direction instead of snapping
                dx = -dx + random.choice([-1, 0, 1]) * 0.5  # Smoother bounce effect
            dy += random.choice([-1, 0, 1])  # Small vertical change
            bounced = True

        # Check if the bird is at the Y edge and adjust direction gradually
        if new_y + win_height >= screen_height or new_y <= 0:
            if dy == 0: 
                dy = random.choice([-5, 5])  # Prevent being stuck by ensuring movement
            else:
                # Gradually change the direction instead of snapping
                dy = -dy + random.choice([-1, 0, 1]) * 0.5  # Smoother bounce effect
            dx += random.choice([-1, 0, 1])  # Small horizontal change
            bounced = True

        # Limit speed to prevent it from getting too fast
        dx = max(min(dx, 7), -7)
        dy = max(min(dy, 7), -7)

        if bounced:
            play()  # Play sound when bouncing

        # Ensure that new_x and new_y are integers
        new_x = int(new_x)
        new_y = int(new_y)

        # Always update window position and schedule the next move
        win.geometry(f"+{new_x}+{new_y}")
        win.after(10, move_window)  # Continue movement every 10ms

    image_list = [
        'hawk.png', 'crow.png', 'walmart hummingbird.png', 'low quality bird.png',
        'dove.png', 'grippers.png', 'blue.png', 'yellow thing.png',
        'hummingbird.png', 'gay dove.png', 'gray thing in ma hand.png', 'cartoon.png'
    ]
    image = random.choice(image_list)

    original = Image.open(resource_path(image))  # ✅ Uses resource_path
    scale = random.uniform(0.3, 1.0)
    new_width = int(original.width * scale)
    new_height = int(original.height * scale)
    resized = original.resize((new_width, new_height), Image.LANCZOS)

    win.image = ImageTk.PhotoImage(resized)
    label = tk.Label(win, image=win.image, bg='white')

    win.overrideredirect(True)
    win.lift()
    win.wm_attributes("-topmost", True)
    win.wm_attributes("-disabled", True)
    win.wm_attributes("-transparentcolor", "white")
    if platform.system() == 'Windows':
        hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
        styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x80000 | 0x20)  # WS_EX_LAYERED | WS_EX_TRANSPARENT
    label.pack()
    
    move_window()

root = tk.Tk()
root.withdraw()

num_birds = random.randint(1, 5)
for _ in range(num_birds):
    makebird()

root.mainloop()