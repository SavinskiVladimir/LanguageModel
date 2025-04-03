import tkinter as tk
from tkinter import scrolledtext

def request(request_text):
    return "Ответ"

def get_request_text():
    pass

def main():
    window = tk.Tk()
    window.title("Языковая модель")
    window.geometry("800x600")
    window.config(bg="white")

    # надпись приглашение ко вводу
    text_entry_label = tk.Label(window, text="Введите ключевую фразу для генерации текста", font=("Calibri", 14))
    text_entry_label.place(x=215, y=280)

    # поле для ввода
    text_entry = tk.Text(window, width = 50, height=8, font=("Calibri", 14))
    text_entry.place(x=160, y=320)

    # кнопка для ввода текста
    text_entry_button = tk.Button(window, text="Получить результат", width=30, height=1, font=("Calibri", 14), borderwidth=2, relief="raised", activebackground="blue", command=lambda: get_request_text())
    text_entry_button.place(x=245, y=520)

    # логотип
    logo_image = tk.PhotoImage(file="files/logo.png")
    logo_image = logo_image.subsample(2, 2)
    logo_label = tk.Label(window, image=logo_image)
    logo_label.place(x=10, y=10)


    # окно для вывода ответа
    response_srcoled = scrolledtext.ScrolledText(window, width=60, height=11, font=("Calibri", 14))
    response_srcoled.insert(tk.END, request("Запрос"))
    response_srcoled.place(x=160, y=15)

    window.mainloop()