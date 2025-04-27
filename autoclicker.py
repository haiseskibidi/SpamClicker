import tkinter as tk
import pyautogui
import keyboard
import threading
import time
import sys
from tkinter import ttk

# Отключаем функцию безопасности PyAutoGUI
pyautogui.FAILSAFE = False

class AutoClicker:
    def __init__(self):
        # Флаги для активации функций
        self.spam_active = False
        self.lmb_active = False
        self.menu_visible = False
        
        # Клавиши для бинда
        self.spam_key = 'f1'  # По умолчанию F1
        self.lmb_key = 'f2'   # По умолчанию F2
        
        # Создаем интерфейс
        self.root = tk.Tk()
        self.root.title("AutoClicker")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # Поверх других окон
        
        # Скрываем меню при запуске
        self.root.withdraw()
        
        # Стиль
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Запускаем потоки
        self.start_threads()
        
        # Регистрируем горячую клавишу для показа/скрытия меню
        keyboard.on_press_key('delete', self.toggle_menu)
        
        # Регистрируем горячие клавиши для функций
        keyboard.on_press_key(self.spam_key, self.toggle_spam_hotkey)
        keyboard.on_press_key(self.lmb_key, self.toggle_lmb_hotkey)
    
    def create_widgets(self):
        # Рамка для Спам-функции
        spam_frame = ttk.LabelFrame(self.root, text="Спам (ЛКМ + Пробел + 1)")
        spam_frame.pack(fill="x", padx=10, pady=10)
        
        # Кнопка для Спам-функции
        self.spam_button = ttk.Button(spam_frame, text="Включить", command=self.toggle_spam)
        self.spam_button.pack(side="left", padx=10, pady=10)
        
        # Рамка для бинда Спам-функции
        spam_bind_frame = ttk.Frame(spam_frame)
        spam_bind_frame.pack(side="right", padx=10, pady=10)
        
        ttk.Label(spam_bind_frame, text="Бинд:").pack(side="left")
        self.spam_bind_label = ttk.Label(spam_bind_frame, text=self.spam_key.upper())
        self.spam_bind_label.pack(side="left", padx=5)
        
        ttk.Button(spam_bind_frame, text="Изменить", command=self.change_spam_bind).pack(side="left", padx=5)
        
        # Рамка для ЛКМ-функции
        lmb_frame = ttk.LabelFrame(self.root, text="Автоклик ЛКМ")
        lmb_frame.pack(fill="x", padx=10, pady=10)
        
        # Кнопка для ЛКМ-функции
        self.lmb_button = ttk.Button(lmb_frame, text="Включить", command=self.toggle_lmb)
        self.lmb_button.pack(side="left", padx=10, pady=10)
        
        # Рамка для бинда ЛКМ-функции
        lmb_bind_frame = ttk.Frame(lmb_frame)
        lmb_bind_frame.pack(side="right", padx=10, pady=10)
        
        ttk.Label(lmb_bind_frame, text="Бинд:").pack(side="left")
        self.lmb_bind_label = ttk.Label(lmb_bind_frame, text=self.lmb_key.upper())
        self.lmb_bind_label.pack(side="left", padx=5)
        
        ttk.Button(lmb_bind_frame, text="Изменить", command=self.change_lmb_bind).pack(side="left", padx=5)
        
        # Информационная рамка
        info_frame = ttk.LabelFrame(self.root, text="Информация")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text="Delete - показать/скрыть меню", font=('Arial', 9)).pack(pady=5)
        ttk.Label(info_frame, text="Внимание: использование может нарушать правила игр", font=('Arial', 8)).pack(pady=5)
    
    def start_threads(self):
        # Поток для спам-функции
        spam_thread = threading.Thread(target=self.spam_function, daemon=True)
        spam_thread.start()
        
        # Поток для функции ЛКМ
        lmb_thread = threading.Thread(target=self.lmb_function, daemon=True)
        lmb_thread.start()
    
    def spam_function(self):
        """Функция для спама (ЛКМ + Пробел + 1)"""
        while True:
            if self.spam_active:
                pyautogui.click()  # ЛКМ
                pyautogui.press('space')  # Пробел
                pyautogui.press('1')  # Клавиша 1
            time.sleep(0.01)  # 10 мс
    
    def lmb_function(self):
        """Функция для автоклика ЛКМ"""
        while True:
            if self.lmb_active:
                pyautogui.click()  # ЛКМ
            time.sleep(0.01)  # 10 мс
    
    def toggle_spam(self):
        """Переключение спам-функции через интерфейс"""
        self.spam_active = not self.spam_active
        if self.spam_active:
            self.spam_button.configure(text="Выключить")
        else:
            self.spam_button.configure(text="Включить")
    
    def toggle_lmb(self):
        """Переключение функции ЛКМ через интерфейс"""
        self.lmb_active = not self.lmb_active
        if self.lmb_active:
            self.lmb_button.configure(text="Выключить")
        else:
            self.lmb_button.configure(text="Включить")
    
    def toggle_spam_hotkey(self, e):
        """Переключение спам-функции через горячую клавишу"""
        self.toggle_spam()
    
    def toggle_lmb_hotkey(self, e):
        """Переключение функции ЛКМ через горячую клавишу"""
        self.toggle_lmb()
    
    def toggle_menu(self, e):
        """Показать/скрыть меню"""
        self.menu_visible = not self.menu_visible
        if self.menu_visible:
            self.root.deiconify()  # Показать окно
        else:
            self.root.withdraw()  # Скрыть окно
    
    def change_spam_bind(self):
        """Изменение бинда для спам-функции"""
        # Создаем диалоговое окно
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменение бинда")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        
        ttk.Label(dialog, text="Нажмите клавишу для бинда...").pack(pady=10)
        
        # Функция для обработки нажатия
        def on_key_press(event):
            key = event.keysym.lower()
            if key != 'escape':  # Если не Escape
                # Отключаем старый бинд
                keyboard.unhook_key(self.spam_key)
                # Устанавливаем новый бинд
                self.spam_key = key
                self.spam_bind_label.configure(text=key.upper())
                keyboard.on_press_key(self.spam_key, self.toggle_spam_hotkey)
            dialog.destroy()
        
        dialog.bind('<Key>', on_key_press)
        dialog.focus_set()
    
    def change_lmb_bind(self):
        """Изменение бинда для функции ЛКМ"""
        # Создаем диалоговое окно
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменение бинда")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        
        ttk.Label(dialog, text="Нажмите клавишу для бинда...").pack(pady=10)
        
        # Функция для обработки нажатия
        def on_key_press(event):
            key = event.keysym.lower()
            if key != 'escape':  # Если не Escape
                # Отключаем старый бинд
                keyboard.unhook_key(self.lmb_key)
                # Устанавливаем новый бинд
                self.lmb_key = key
                self.lmb_bind_label.configure(text=key.upper())
                keyboard.on_press_key(self.lmb_key, self.toggle_lmb_hotkey)
            dialog.destroy()
        
        dialog.bind('<Key>', on_key_press)
        dialog.focus_set()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = AutoClicker()
        app.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1) 