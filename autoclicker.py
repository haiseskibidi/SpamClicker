import tkinter as tk
import pyautogui
import threading
import time
import sys
import ctypes
from tkinter import ttk
from pynput import keyboard as kb
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

pyautogui.FAILSAFE = False

class AutoClicker:
    def __init__(self):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.spam_active = False
        self.lmb_active = False
        self.menu_visible = False
        self.program_enabled = True
        
        self.spam_key = Key.f1
        self.lmb_key = Key.f2
        self.menu_key = Key.delete
        
        self.spam_key_str = 'F1'
        self.lmb_key_str = 'F2'
        
        self.root = tk.Tk()
        self.root.title("AutoClicker")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        self.root.withdraw()
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('Program.TButton', font=('Arial', 11, 'bold'))
        
        self.create_widgets()
        self.start_threads()
        self.setup_keyboard_listener()
    
    def create_widgets(self):
        program_frame = ttk.LabelFrame(self.root, text="Program Control")
        program_frame.pack(fill="x", padx=10, pady=10)
        
        self.program_button = ttk.Button(
            program_frame, 
            text="Disable Program", 
            command=self.toggle_program,
            style='Program.TButton'
        )
        self.program_button.pack(padx=10, pady=10, fill="x")
        
        self.status_label = ttk.Label(
            program_frame, 
            text="Status: ACTIVE", 
            font=('Arial', 10, 'bold'),
            foreground='green'
        )
        self.status_label.pack(side="left", padx=10)
        
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=10, pady=5)
        
        spam_frame = ttk.LabelFrame(self.root, text="Spam (LMB + Space + 1)")
        spam_frame.pack(fill="x", padx=10, pady=10)
        self.spam_button = ttk.Button(spam_frame, text="Enable", command=self.toggle_spam)
        self.spam_button.pack(side="left", padx=10, pady=10)
        spam_bind_frame = ttk.Frame(spam_frame)
        spam_bind_frame.pack(side="right", padx=10, pady=10)
        ttk.Label(spam_bind_frame, text="Bind:").pack(side="left")
        self.spam_bind_label = ttk.Label(spam_bind_frame, text=self.spam_key_str)
        self.spam_bind_label.pack(side="left", padx=5)
        ttk.Button(spam_bind_frame, text="Change", command=self.change_spam_bind).pack(side="left", padx=5)
        lmb_frame = ttk.LabelFrame(self.root, text="Auto LMB Click")
        lmb_frame.pack(fill="x", padx=10, pady=10)
        self.lmb_button = ttk.Button(lmb_frame, text="Enable", command=self.toggle_lmb)
        self.lmb_button.pack(side="left", padx=10, pady=10)
        lmb_bind_frame = ttk.Frame(lmb_frame)
        lmb_bind_frame.pack(side="right", padx=10, pady=10)
        ttk.Label(lmb_bind_frame, text="Bind:").pack(side="left")
        self.lmb_bind_label = ttk.Label(lmb_bind_frame, text=self.lmb_key_str)
        self.lmb_bind_label.pack(side="left", padx=5)
        ttk.Button(lmb_bind_frame, text="Change", command=self.change_lmb_bind).pack(side="left", padx=5)
        info_frame = ttk.LabelFrame(self.root, text="Information")
        info_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(info_frame, text="Delete - show/hide menu", font=('Arial', 9)).pack(pady=2)
        ttk.Label(info_frame, text="Running as admin: " + ("Yes" if is_admin() else "No"), font=('Arial', 9)).pack(pady=2)
        ttk.Label(info_frame, text="Warning: using may violate game rules", font=('Arial', 8)).pack(pady=2)
    
    def setup_keyboard_listener(self):
        def on_press(key):
            try:
                if key == self.menu_key:
                    self.toggle_menu()
                
                if self.program_enabled:
                    if key == self.spam_key:
                        self.toggle_spam()
                    if key == self.lmb_key:
                        self.toggle_lmb()
            except:
                pass
            return True
        
        self.keyboard_listener = kb.Listener(on_press=on_press)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()
    
    def start_threads(self):
        spam_thread = threading.Thread(target=self.spam_function, daemon=True)
        spam_thread.start()
        lmb_thread = threading.Thread(target=self.lmb_function, daemon=True)
        lmb_thread.start()
    
    def spam_function(self):
        while True:
            if self.spam_active and self.program_enabled:
                self.mouse.press(Button.left)
                self.mouse.release(Button.left)
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
                self.keyboard.press('1')
                self.keyboard.release('1')
            time.sleep(0.01)
    
    def lmb_function(self):
        while True:
            if self.lmb_active and self.program_enabled:
                self.mouse.press(Button.left)
                self.mouse.release(Button.left)
            time.sleep(0.01)
    
    def toggle_program(self):
        self.program_enabled = not self.program_enabled
        
        if self.program_enabled:
            self.program_button.configure(text="Disable Program")
            self.status_label.configure(text="Status: ACTIVE", foreground='green')
        else:
            self.program_button.configure(text="Enable Program")
            self.status_label.configure(text="Status: DISABLED", foreground='red')
    
    def toggle_spam(self):
        self.spam_active = not self.spam_active
        if self.menu_visible:
            if self.spam_active:
                self.spam_button.configure(text="Disable")
            else:
                self.spam_button.configure(text="Enable")
    
    def toggle_lmb(self):
        self.lmb_active = not self.lmb_active
        if self.menu_visible:
            if self.lmb_active:
                self.lmb_button.configure(text="Disable")
            else:
                self.lmb_button.configure(text="Enable")
    
    def toggle_menu(self):
        self.menu_visible = not self.menu_visible
        if self.menu_visible:
            self.root.deiconify()
            if self.spam_active:
                self.spam_button.configure(text="Disable")
            else:
                self.spam_button.configure(text="Enable")
            if self.lmb_active:
                self.lmb_button.configure(text="Disable")
            else:
                self.lmb_button.configure(text="Enable")
        else:
            self.root.withdraw()
    
    def key_to_string(self, key):
        if hasattr(key, '_name_'):
            return key._name_.upper()
        else:
            return key.char.upper()
    
    def change_spam_bind(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Change bind")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        ttk.Label(dialog, text="Press a key for bind...").pack(pady=10)
        
        def on_key_press(key):
            listener.stop()
            if key != kb.Key.esc:
                self.spam_key = key
                self.spam_key_str = self.key_to_string(key)
                self.spam_bind_label.configure(text=self.spam_key_str)
            dialog.destroy()
            return False
        
        listener = kb.Listener(on_press=on_key_press)
        listener.start()
        dialog.focus_set()
    
    def change_lmb_bind(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Change bind")
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        ttk.Label(dialog, text="Press a key for bind...").pack(pady=10)
        
        def on_key_press(key):
            listener.stop()
            if key != kb.Key.esc:
                self.lmb_key = key
                self.lmb_key_str = self.key_to_string(key)
                self.lmb_bind_label.configure(text=self.lmb_key_str)
            dialog.destroy()
            return False
        
        listener = kb.Listener(on_press=on_key_press)
        listener.start()
        dialog.focus_set()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        if sys.platform.startswith('win'):
            run_as_admin()
        app = AutoClicker()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 