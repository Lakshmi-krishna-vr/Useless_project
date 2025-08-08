import time
import pygetwindow as gw
import tkinter  as tk
import pyautogui

TARGET_APP_KEYWORD = "YouTube"  # Change if needed
CHECK_INTERVAL = 1  # seconds
TRIGGER_DELAY = 10  # seconds

questions = [
    "poi vallom pani cheyy penne  ?",
    "Did you finish your work?",
    "Shouldn't you take a break?"
]

def interrupt_popup():
    # Pause video before popup
    pyautogui.press('space')

    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-fullscreen', True)
    root.configure(bg="black")
    root.focus_force()

    question_index = 0
    label = tk.Label(root, text=questions[question_index], fg="white", bg="black", font=("Arial", 24))
    label.pack(pady=50)

    def answer(_):
        nonlocal question_index
        question_index += 1
        if question_index >= len(questions):
            root.destroy()
        else:
            label.config(text=questions[question_index])

    yes_btn = tk.Button(root, text="Yes", command=lambda: answer("Yes"), font=("Arial", 20))
    yes_btn.pack(side="left", padx=50)

    no_btn = tk.Button(root, text="No", command=lambda: answer("No"), font=("Arial", 20))
    no_btn.pack(side="right", padx=50)

    root.mainloop()

def monitor():
    while True:
        active_window = gw.getActiveWindow()
        if active_window and TARGET_APP_KEYWORD.lower() in active_window.title.lower():
            print(f"Detected {TARGET_APP_KEYWORD}, waiting {TRIGGER_DELAY}s...")
            time.sleep(TRIGGER_DELAY)
            interrupt_popup()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
