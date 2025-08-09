import time
import pygetwindow as gw
import pyautogui
from PIL import Image, ImageTk, ImageFilter
import tkinter as tk

# ====== SETTINGS ======
TARGET_APP_KEYWORD = "YouTube"  # keyword to detect
TRIGGER_DELAY = 10  # seconds
CHECK_INTERVAL = 1  # seconds
CARTOON_IMAGE_PATH = "C:\opencv\maman-removebg-preview.png"  # transparent PNG
QUESTIONS = [
    "joli onum ayilee",
    "Hey! Are you sure you want to keep watching?",
    "Did you finish your work?",
    "How about a break?"
]
# ======================

screen_width, screen_height = pyautogui.size()
image_width, image_height = 300, 300  # cartoon size

# Predefined positions
POSITIONS = [
    (0, 0),
    (screen_width - image_width, 0),
    (0, screen_height - image_height),
    (screen_width - image_width, screen_height - image_height)
]

def create_interrupt():
    # Pause video
    pyautogui.press('space')

    # Screenshot & blur
    screenshot = pyautogui.screenshot().convert("RGB")
    blurred = screenshot.filter(ImageFilter.GaussianBlur(10))

    # Load transparent PNG
    try:
        cartoon = Image.open(CARTOON_IMAGE_PATH).convert("RGBA")
        cartoon = cartoon.resize((image_width, image_height), Image.LANCZOS)
    except Exception as e:
        print(f"Error loading cartoon image: {e}")
        return

    # Tkinter window
    root = tk.Tk()
    root.title("Interrupt")
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)

    # Position tracking
    position_index = 0
    question_index = 0

    # Merge cartoon onto blurred background (keeps transparency)
    def merge_images():
        merged = blurred.copy()
        x, y = POSITIONS[position_index]
        merged.paste(cartoon, (x, y), cartoon)  # mask=cartoon keeps transparency
        return ImageTk.PhotoImage(merged)

    # Initial background with cartoon
    combined_img = merge_images()
    bg_label = tk.Label(root, image=combined_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Question label
    question_label = tk.Label(
        root, text=QUESTIONS[question_index],
        fg="white", bg="black",
        font=("Arial", 24), wraplength=800, justify="left"
    )
    question_label.place(x=400, y=250)

    # Button handler
    def answer(_):
        nonlocal question_index, position_index, combined_img
        question_index += 1
        if question_index >= len(QUESTIONS):
            root.destroy()
        else:
            question_label.config(text=QUESTIONS[question_index])
            position_index = (position_index + 1) % len(POSITIONS)
            combined_img = merge_images()
            bg_label.config(image=combined_img)
            bg_label.image = combined_img  # prevent GC

    # Buttons
    yes_btn = tk.Button(root, text="Yes", command=lambda: answer("Yes"), font=("Arial", 18))
    yes_btn.place(x=400, y=400)

    no_btn = tk.Button(root, text="No", command=lambda: answer("No"), font=("Arial", 18))
    no_btn.place(x=500, y=400)

    root.mainloop()

def monitor():
    while True:
        active_window = gw.getActiveWindow()
        if active_window and TARGET_APP_KEYWORD.lower() in active_window.title.lower():
            print(f"Detected {TARGET_APP_KEYWORD}, waiting {TRIGGER_DELAY}s...")
            time.sleep(TRIGGER_DELAY)
            create_interrupt()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
