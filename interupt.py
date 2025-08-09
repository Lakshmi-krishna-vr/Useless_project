import time
import pygetwindow as gw
import pyautogui
from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
import webbrowser

# ====== SETTINGS ======
APPS = {
    "youtube": {
        "first": "മോനെ....YOUTUBE കാണു ആണോ ???",
        "follow": "ഇതൊക്കെ കണ്ട് ഇരുന്ന മതിയോ "
    },
    "instagram": {
        "first": "മോനെ....INSTA കാണു ആണോ ???",
        "follow": "ഇതൊക്കെ കണ്ട് ഇരുന്ന മതിയോ "
    },
    "facebook": {
        "first": "മോനെ....FACEBOOK കാണു ആണോ ???",
        "follow": "ഇതൊക്കെ കണ്ട് ഇരുന്ന മതിയോ "
    },
    "geeksforgeeks": {
        "first": "അപ്പൊ മോന് ഇരുന്നു പേടിച്ചോ മാമൻ പോട്ടേ !"
    }
}

COMMON_QUESTIONS = [
    "ജോലി ഒന്നും ആയിലെ??",
    "മാമനോട് ഒന്നും തോന്നല്ലേ കേട്ടോ",
    "SUPPLI ഒക്കെ എഴുതി എടുത്തോ?",
    "പോയി പഠിച്ചുടെ??",
    "ഇങ്ങനെ ഒക്കെ നടന്നാ മതിയോ?",
    "വേറെ പണി ഒന്നും ഇല്ലേ ??",
    "മാമനോട് ഒന്നും തോന്നല്ലേ കേട്ടോ",
    "എന്നാ മാമൻ പോട്ടേ ??",
    "അങ്ങനെ അങ് പോവാൻ പറ്റുവോ",
    "മോൻ ഇതുവരെ പോയില്ലേ??",
    "ബാ മാമൻ തന്നെ കൊണ്ട്  പോവാം"
]

TRIGGER_DELAY = 5  # seconds before showing interrupt
CHECK_INTERVAL = 1  # seconds between checks
CARTOON_IMAGE_PATH = r"C:\opencv\maman-removebg-preview.png"  # transparent PNG
# ======================

# Get screen size
screen_width, screen_height = pyautogui.size()

# Base image size before scaling
image_width, image_height = 300, 300

# Predefined positions
POSITIONS = [
    (0, 0),
    (screen_width - image_width, 0),
    (0, screen_height - image_height),
    (screen_width - image_width, screen_height - image_height)
]


def create_interrupt(app_key):
    pyautogui.press('space')  # Pause video

    # Screenshot & blur
    screenshot = pyautogui.screenshot().convert("RGB")
    blurred = screenshot.filter(ImageFilter.GaussianBlur(10))

    # Load transparent PNG
    try:
        cartoon = Image.open(CARTOON_IMAGE_PATH).convert("RGBA")
    except Exception as e:
        print(f"Error loading cartoon image: {e}")
        return

    # Scale image
    scale_factor = 1.5
    new_size = (int(image_width * scale_factor), int(image_height * scale_factor))
    cartoon = cartoon.resize(new_size, Image.LANCZOS)

    root = tk.Tk()
    root.title("Interrupt")
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)

    position_index = 0
    stage = 0

    questions = [APPS[app_key]["first"]]

    def merge_images():
        merged = blurred.copy()
        x, y = POSITIONS[position_index]
        merged.paste(cartoon, (x, y), cartoon)
        return ImageTk.PhotoImage(merged)

    combined_img = merge_images()
    bg_label = tk.Label(root, image=combined_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    speech_frame = tk.Frame(root, bg="black", padx=10, pady=10)
    question_label = tk.Label(
        speech_frame,
        text=questions[0],
        fg="white", bg="black",
        font=("Arial", 18),
        wraplength=300,
        justify="left"
    )
    question_label.pack()

    btn_frame = tk.Frame(speech_frame, bg="black")
    btn_frame.pack(pady=5)

    if app_key == "geeksforgeeks":
        # Just one "OK" button
        ok_btn = tk.Button(
            btn_frame, text="OK", font=("Arial", 14),
            command=root.destroy
        )
        ok_btn.pack(padx=5)
    else:
        def answer(ans):
            nonlocal stage, combined_img, position_index, questions
            if stage == 0:
                if ans == "Yes":
                    questions.append(APPS[app_key]["follow"])
                else:
                    questions.append("what else are you doing?")
                questions.extend(COMMON_QUESTIONS)
                stage += 1
                question_label.config(text=questions[stage])
            else:
                stage += 1
                if stage >= len(questions):
                    webbrowser.open("https://www.geeksforgeeks.org")
                    root.destroy()
                    return
                question_label.config(text=questions[stage])

            position_index = (position_index + 1) % len(POSITIONS)
            combined_img = merge_images()
            bg_label.config(image=combined_img)
            bg_label.image = combined_img
            move_speech()

        yes_btn = tk.Button(btn_frame, text="Yes", command=lambda: answer("Yes"), font=("Arial", 14))
        yes_btn.pack(side="left", padx=5)

        no_btn = tk.Button(btn_frame, text="No", command=lambda: answer("No"), font=("Arial", 14))
        no_btn.pack(side="left", padx=5)

    def move_speech():
        x, y = POSITIONS[position_index]
        speech_x = x + new_size[0] + 10 if x < screen_width // 2 else x - 320
        speech_y = y
        speech_frame.place(x=speech_x, y=speech_y)

    move_speech()
    root.mainloop()

shown_once = {key: False for key in APPS.keys()}

def monitor():
    while True:
        active_window = gw.getActiveWindow()
        if active_window:
            title = active_window.title.lower()
            for app_key in APPS.keys():
                if app_key in title:
                    if app_key == "geeksforgeeks" and shown_once[app_key]:
                        continue  # Skip if already shown
                    print(f"Detected {app_key}, waiting {TRIGGER_DELAY}s...")
                    time.sleep(TRIGGER_DELAY)
                    create_interrupt(app_key)
                    shown_once[app_key] = True
                    break
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor()
 