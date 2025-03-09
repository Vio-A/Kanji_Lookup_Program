import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import sys
import os

# This fixes those blurry windows I often see; scaling issue
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def get_kanji_info(kanji):
    url = f"https://kanjiapi.dev/v1/kanji/{kanji}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

#kanji only
def is_valid_kanji(character):
    return '\u4e00' <= character <= '\u9faf'

def fetch_kanji_info():
    kanji = entry.get().strip()
    if not kanji or not is_valid_kanji(kanji):
        messagebox.showerror("エラー", "漢字を")
        return
    
    kanji_info = get_kanji_info(kanji)
    if kanji_info:
        result_text = (
            f"漢字：{kanji_info.get('kanji')}\n"
            f"学年：{kanji_info.get('grade')}\n"
            f"画数：{kanji_info.get('stroke_count')}\n"
            f"意味：{', '.join(kanji_info.get('meanings', []))}\n"
            f"訓読み：{', '.join(kanji_info.get('kun_readings', []))}\n"
            f"音読み：{', '.join(kanji_info.get('on_readings', []))}\n"
            f"JLPTレベル:{kanji_info.get('jlpt')}\n"
        )
        result_label.config(text=result_text)

def show_credits():
    credits_text = (
        "Program by Vio-A\n"
        "Image by Alethea Flowers from Pixabay\n"
        "API: KanjiAPI (https://kanjiapi.dev/)\n"
    )
    messagebox.showinfo("感謝", credits_text)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

root = tk.Tk()
root.title("漢字検索")
root.iconbitmap(resource_path("Assets/Images/Robinweatherall-Chocolate-Mint-leaf.ico"))

window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

bg_image = Image.open(resource_path("Assets/Images/lantern-7897815_1280.jpg"))
bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

entry = tk.Entry(root, width=50, bg="#33522d", fg="#ffffff", insertbackground="#7ba66a", borderwidth=0, relief="flat", highlightthickness=0, justify="center")
canvas.create_window(window_width // 2, 80, window=entry)
entry.focus_set()

button = tk.Button(root, text="検索", command=fetch_kanji_info, bg="#33522d", fg="#ffffff", activebackground="#B0C4B1", activeforeground="#7ba66a", borderwidth=0, padx=4, pady=4)
canvas.create_window(window_width // 2, 150, window=button)

credits_button = tk.Button(root, text="感謝", command=show_credits, bg="#33522d", fg="#ffffff", activebackground="#B0C4B1", activeforeground="#7ba66a", borderwidth=0, padx=4, pady=4)
canvas.create_window(window_width // 2, 560, window=credits_button)

result_label = tk.Label(root, text="", justify=tk.LEFT, bg="#33522d", fg="#ffffff", borderwidth=0, relief="flat", padx=10, pady=10)
canvas.create_window(window_width // 2, 300, window=result_label)

entry.bind('<Return>', lambda event: fetch_kanji_info())

root.mainloop()