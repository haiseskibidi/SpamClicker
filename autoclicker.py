import sys
import os
import time
import threading
import ctypes
import json
import customtkinter as ctk

pyautogui = None
kb = None
Button = None
MouseController = None
KeyboardController = None
Key = None

def lazy_import():
    global pyautogui, kb, Button, MouseController, KeyboardController, Key
    if pyautogui is None:
        import pyautogui
        pyautogui.FAILSAFE = False
    if kb is None:
        from pynput import keyboard as kb
    if Button is None or MouseController is None:
        from pynput.mouse import Button, Controller as MouseController
    if Key is None or KeyboardController is None:
        from pynput.keyboard import Key, Controller as KeyboardController

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not sys.platform.startswith('win'):
        return
        
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

class NeumorphicFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        is_dark = ctk.get_appearance_mode() == "Dark"
        
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = "#2d3035" if is_dark else "#e0e5ec"
        
        if "border_width" not in kwargs:
            kwargs["border_width"] = 0
            
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = 14
            
        super().__init__(master, **kwargs)
        
        self.inner_frame = ctk.CTkFrame(
            self, 
            fg_color=kwargs["fg_color"],
            corner_radius=kwargs["corner_radius"] - 2 if kwargs["corner_radius"] > 2 else 0,
            border_width=0
        )
        self.inner_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.container = ctk.CTkFrame(
            self.inner_frame,
            fg_color="transparent",
            corner_radius=0,
            border_width=0
        )
        self.container.pack(fill="both", expand=True, padx=8, pady=8)
    
    def add_widget(self, widget):
        widget.pack(in_=self.container, **widget.pack_info())

class NeumorphicButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        is_dark = ctk.get_appearance_mode() == "Dark"
        
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = "#2d3035" if is_dark else "#e0e5ec"
            
        if "text_color" not in kwargs:
            kwargs["text_color"] = "#DCE4EE" if is_dark else "#2D3035"
            
        if "hover_color" not in kwargs:
            kwargs["hover_color"] = "#35393f" if is_dark else "#d1d6dd"
            
        if "border_width" not in kwargs:
            kwargs["border_width"] = 0
            
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = 12
        
        self.is_active = kwargs.pop("is_active", False)
        self.active_color = kwargs.pop("active_color", "#4870b8" if is_dark else "#5790d6")
        
        super().__init__(master, **kwargs)
        
        self.original_fg = kwargs["fg_color"]
        self.original_hover = kwargs["hover_color"]
        
        if self.is_active:
            self.configure(fg_color=self.active_color)
    
    def set_active(self, active):
        self.is_active = active
        if active:
            self.configure(fg_color=self.active_color)
        else:
            self.configure(fg_color=self.original_fg)

class AutoClicker:
    def __init__(self):
        lazy_import()
        
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.spam_active = False
        self.lmb_active = False
        self.custom_active = False
        self.menu_visible = True
        self.program_enabled = True
        self.pressed_keys_lock = threading.Lock()
        self.currently_pressed_keys = set()
        
        self.custom_sequence = []
        self.custom_key = Key.f3
        self.custom_key_str = 'F3'
        
        self.spam_key = Key.f1
        self.lmb_key = Key.f2
        self.menu_key = Key.delete
        
        self.spam_key_str = 'F1'
        self.lmb_key_str = 'F2'
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_neumorphic_colors()
        
        self.root = ctk.CTk()
        self.root.title("AutoClicker")
        self.root.geometry("500x750")
        self.root.minsize(500, 750)
        self.root.resizable(True, True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 1.0)
        
        self.create_widgets()
        self.start_threads()
        self.setup_keyboard_listener()
    
    def setup_neumorphic_colors(self):
        self.light_colors = {
            'bg': '#e0e5ec',
            'shadow_dark': '#a3b1c6',
            'shadow_light': '#ffffff',
            'text': '#2D3035',
            'accent': '#5790d6',
            'danger': '#e63e3e',
            'success': '#32a852',
            'surface': '#e0e5ec',
            'hover': '#d1d6dd'
        }
        
        self.dark_colors = {
            'bg': '#2d3035',
            'shadow_dark': '#202227',
            'shadow_light': '#3a3e46',
            'text': '#DCE4EE',
            'accent': '#4870b8',
            'danger': '#bd3939',
            'success': '#288c42',
            'surface': '#2d3035',
            'hover': '#35393f'
        }
        
    def get_colors(self):
        return self.dark_colors if ctk.get_appearance_mode() == "Dark" else self.light_colors
    
    def create_widgets(self):
        colors = self.get_colors()
        
        main_frame = ctk.CTkFrame(self.root, fg_color=colors['bg'], corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        
        content_scroll = ctk.CTkScrollableFrame(main_frame, fg_color=colors['bg'], corner_radius=0)
        content_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        content_frame = ctk.CTkFrame(content_scroll, fg_color=colors['bg'], corner_radius=0)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        header_frame = NeumorphicFrame(content_frame, fg_color=colors['bg'])
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_container = ctk.CTkFrame(header_frame.container, fg_color="transparent")
        title_container.pack(fill="x", padx=15, pady=15)
        
        title_left_frame = ctk.CTkFrame(title_container, fg_color="transparent")
        title_left_frame.pack(side="left")
        
        app_title = ctk.CTkLabel(
            title_left_frame, 
            text="AutoClicker", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors['text']
        )
        app_title.pack(anchor="w")
        
        version_label = ctk.CTkLabel(
            title_left_frame,
            text="v2.0",
            font=ctk.CTkFont(size=13),
            text_color=colors['text']
        )
        version_label.pack(anchor="w")
        
        author_label = ctk.CTkLabel(
            title_container,
            text="by zaaaa",
            font=ctk.CTkFont(size=14),
            text_color=colors['text']
        )
        author_label.pack(side="right")
        
        program_frame = NeumorphicFrame(content_frame, fg_color=colors['bg'])
        program_frame.pack(fill="x", pady=(0, 10))
        
        program_container = ctk.CTkFrame(program_frame.container, fg_color="transparent")
        program_container.pack(fill="x", padx=15)
        
        program_label = ctk.CTkLabel(
            program_container,
            text="Program Control",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=colors['text']
        )
        program_label.pack(anchor="w", pady=(0, 10))
        
        control_container = ctk.CTkFrame(program_container, fg_color="transparent")
        control_container.pack(fill="x")
        
        status_frame = ctk.CTkFrame(control_container, fg_color="transparent")
        status_frame.pack(side="left")
        
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=22),
            text_color=colors['success']
        )
        self.status_indicator.pack(side="left")
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="ACTIVE",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors['success']
        )
        self.status_label.pack(side="left", padx=5)
        
        self.program_button = NeumorphicButton(
            control_container,
            text="Disable Program",
            font=ctk.CTkFont(size=15),
            height=40,
            fg_color=colors['surface'],
            text_color=colors['danger'],
            hover_color=colors['hover'],
            command=self.toggle_program
        )
        self.program_button.pack(side="right")
        
        functions_frame = NeumorphicFrame(content_frame, fg_color=colors['bg'])
        functions_frame.pack(fill="x", pady=(0, 20))
        
        functions_container = ctk.CTkFrame(functions_frame.container, fg_color="transparent")
        functions_container.pack(fill="x", padx=15, pady=15)
        
        functions_label = ctk.CTkLabel(
            functions_container,
            text="Functions:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=colors['text']
        )
        functions_label.pack(anchor="w", pady=(0, 15))
        
        spam_container = ctk.CTkFrame(functions_container, fg_color="transparent")
        spam_container.pack(fill="x", pady=(0, 15))
        
        spam_title_frame = ctk.CTkFrame(spam_container, fg_color="transparent")
        spam_title_frame.pack(fill="x")
        
        spam_icon = ctk.CTkLabel(
            spam_title_frame,
            text="⌨️",
            font=ctk.CTkFont(size=18),
            text_color=colors['text']
        )
        spam_icon.pack(side="left")
        
        spam_title = ctk.CTkLabel(
            spam_title_frame,
            text="Spam (Space + 1 + LMB)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors['text']
        )
        spam_title.pack(side="left", padx=5)
        
        spam_note_frame = ctk.CTkFrame(spam_container, fg_color="transparent")
        spam_note_frame.pack(fill="x", pady=(2, 0))
        
        spam_note = ctk.CTkLabel(
            spam_note_frame,
            text="For skipping dialogues in Honkai: Star Rail   ",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=colors['text']
        )
        spam_note.pack(side="left", padx=50)
        
        spam_controls = ctk.CTkFrame(spam_container, fg_color="transparent")
        spam_controls.pack(fill="x", pady=10)
        
        self.spam_button = NeumorphicButton(
            spam_controls,
            text="Enable",
            font=ctk.CTkFont(size=14),
            width=120,
            height=36,
            fg_color=colors['surface'],
            text_color=colors['accent'],
            hover_color=colors['hover'],
            command=self.toggle_spam
        )
        self.spam_button.pack(side="left")
        
        bind_frame = ctk.CTkFrame(spam_controls, fg_color="transparent")
        bind_frame.pack(side="right")
        
        bind_label = ctk.CTkLabel(
            bind_frame,
            text="Bind:",
            font=ctk.CTkFont(size=14),
            text_color=colors['text']
        )
        bind_label.pack(side="left")
        
        self.spam_bind_label = ctk.CTkLabel(
            bind_frame,
            text=self.spam_key_str,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors['accent']
        )
        self.spam_bind_label.pack(side="left", padx=5)
        
        spam_bind_button = NeumorphicButton(
            bind_frame,
            text="Change",
            font=ctk.CTkFont(size=13),
            width=80,
            height=30,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=self.change_spam_bind
        )
        spam_bind_button.pack(side="left", padx=5)
        
        lmb_container = ctk.CTkFrame(functions_container, fg_color="transparent")
        lmb_container.pack(fill="x", pady=(0, 15))
        
        lmb_title_frame = ctk.CTkFrame(lmb_container, fg_color="transparent")
        lmb_title_frame.pack(fill="x")
        
        lmb_icon = ctk.CTkLabel(
            lmb_title_frame,
            text="🖱️",
            font=ctk.CTkFont(size=18),
            text_color=colors['text']
        )
        lmb_icon.pack(side="left")
        
        lmb_title = ctk.CTkLabel(
            lmb_title_frame,
            text="Auto-click LMB",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors['text']
        )
        lmb_title.pack(side="left", padx=5)
        
        lmb_controls = ctk.CTkFrame(lmb_container, fg_color="transparent")
        lmb_controls.pack(fill="x", pady=10)
        
        self.lmb_button = NeumorphicButton(
            lmb_controls,
            text="Enable",
            font=ctk.CTkFont(size=14),
            width=120,
            height=36,
            fg_color=colors['surface'],
            text_color=colors['accent'],
            hover_color=colors['hover'],
            command=self.toggle_lmb
        )
        self.lmb_button.pack(side="left")
        
        lmb_bind_frame = ctk.CTkFrame(lmb_controls, fg_color="transparent")
        lmb_bind_frame.pack(side="right")
        
        lmb_bind_label = ctk.CTkLabel(
            lmb_bind_frame,
            text="Bind:",
            font=ctk.CTkFont(size=14),
            text_color=colors['text']
        )
        lmb_bind_label.pack(side="left")
        
        self.lmb_bind_label = ctk.CTkLabel(
            lmb_bind_frame,
            text=self.lmb_key_str,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors['accent']
        )
        self.lmb_bind_label.pack(side="left", padx=5)
        
        lmb_bind_button = NeumorphicButton(
            lmb_bind_frame,
            text="Change",
            font=ctk.CTkFont(size=13),
            width=80,
            height=30,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=self.change_lmb_bind
        )
        lmb_bind_button.pack(side="left", padx=5)
        
        custom_container = ctk.CTkFrame(functions_container, fg_color="transparent")
        custom_container.pack(fill="x")
        
        custom_title_frame = ctk.CTkFrame(custom_container, fg_color="transparent")
        custom_title_frame.pack(fill="x")
        
        custom_icon = ctk.CTkLabel(
            custom_title_frame,
            text="🔧",
            font=ctk.CTkFont(size=18),
            text_color=colors['text']
        )
        custom_icon.pack(side="left")
        
        custom_title = ctk.CTkLabel(
            custom_title_frame,
            text="Custom Sequence",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors['text']
        )
        custom_title.pack(side="left", padx=30)
        
        custom_controls = ctk.CTkFrame(custom_container, fg_color="transparent")
        custom_controls.pack(fill="x", pady=10)
        
        self.custom_button = NeumorphicButton(
            custom_controls,
            text="Enable",
            font=ctk.CTkFont(size=14),
            width=120,
            height=36,
            fg_color=colors['surface'],
            text_color=colors['accent'],
            hover_color=colors['hover'],
            command=self.toggle_custom
        )
        self.custom_button.pack(side="left")
        
        custom_bind_frame = ctk.CTkFrame(custom_controls, fg_color="transparent")
        custom_bind_frame.pack(side="right")
        
        custom_bind_label = ctk.CTkLabel(
            custom_bind_frame,
            text="Bind:",
            font=ctk.CTkFont(size=14),
            text_color=colors['text']
        )
        custom_bind_label.pack(side="left")
        
        self.custom_bind_label = ctk.CTkLabel(
            custom_bind_frame,
            text=self.custom_key_str,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors['accent']
        )
        self.custom_bind_label.pack(side="left", padx=5)
        
        custom_bind_button = NeumorphicButton(
            custom_bind_frame,
            text="Change",
            font=ctk.CTkFont(size=13),
            width=80,
            height=30,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=self.change_custom_bind
        )
        custom_bind_button.pack(side="left", padx=5)
        
        custom_settings_frame = ctk.CTkFrame(custom_container, fg_color="transparent")
        custom_settings_frame.pack(fill="x", pady=(5, 0))
        
        custom_settings_button = NeumorphicButton(
            custom_settings_frame,
            text="Configure Sequence",
            font=ctk.CTkFont(size=14),
            width=250,
            height=36,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=self.open_custom_settings
        )
        custom_settings_button.pack(side="left")
        
        keys_frame = NeumorphicFrame(content_frame, fg_color=colors['bg'])
        keys_frame.pack(fill="x", pady=(0, 20))
        
        keys_container = ctk.CTkFrame(keys_frame.container, fg_color="transparent")
        keys_container.pack(fill="x", padx=15, pady=15)
        
        keys_label = ctk.CTkLabel(
            keys_container,
            text="Hotkeys",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=colors['text']
        )
        keys_label.pack(anchor="w", pady=(0, 10))
        
        key_table = [
            (f"{self.spam_key_str}", "Enable/disable spam"),
            (f"{self.lmb_key_str}", "Enable/disable auto-click"),
            (f"{self.custom_key_str}", "Enable/disable custom sequence"),
            ("Delete", "Show/hide menu")
        ]
        
        for key, desc in key_table:
            row = ctk.CTkFrame(keys_container, fg_color="transparent")
            row.pack(fill="x", pady=3)
            
            key_label = ctk.CTkLabel(
                row,
                text=key,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=colors['accent'],
                width=60
            )
            key_label.pack(side="left", padx=5)
            
            arrow = ctk.CTkLabel(
                row,
                text="→",
                font=ctk.CTkFont(size=14),
                text_color=colors['text'],
                width=20
            )
            arrow.pack(side="left")
            
            desc_label = ctk.CTkLabel(
                row,
                text=desc,
                font=ctk.CTkFont(size=14),
                text_color=colors['text']
            )
            desc_label.pack(side="left", padx=5)
        
        info_frame = NeumorphicFrame(content_frame, fg_color=colors['bg'])
        info_frame.pack(fill="x")
        
        info_container = ctk.CTkFrame(info_frame.container, fg_color="transparent")
        info_container.pack(fill="x", padx=15, pady=15)
        
        info_label = ctk.CTkLabel(
            info_container,
            text="Information",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=colors['text']
        )
        info_label.pack(anchor="w", pady=(0, 10))
        
        admin_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        admin_frame.pack(fill="x", pady=3)
        
        admin_status = "Yes" if is_admin() else "No"
        admin_color = colors['success'] if is_admin() else colors['danger']
        admin_icon = "✓" if is_admin() else "✗"
        
        admin_icon_label = ctk.CTkLabel(
            admin_frame,
            text=admin_icon,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=admin_color
        )
        admin_icon_label.pack(side="left")
        
        admin_text = ctk.CTkLabel(
            admin_frame,
            text=f"Run as administrator: {admin_status}",
            font=ctk.CTkFont(size=14),
            text_color=colors['text']
        )
        admin_text.pack(side="left", padx=5)
        
        warning_box = NeumorphicFrame(info_container, fg_color=colors['bg'])
        warning_box.pack(fill="x", pady=10)
        
        warning_container = ctk.CTkFrame(warning_box.container, fg_color="transparent")
        warning_container.pack(fill="x", padx=5, pady=5)
        
        warning_icon = ctk.CTkLabel(
            warning_container,
            text="⚠️",
            font=ctk.CTkFont(size=16),
            text_color=colors['danger']
        )
        warning_icon.pack(side="left", padx=(0, 5))
        
        warning_text = ctk.CTkLabel(
            warning_container,
            text="Using this program may violate game rules",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color=colors['text']
        )
        warning_text.pack(side="left")
        
        footer_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(5, 0))
    
    def setup_keyboard_listener(self):
        def on_press(key):
            try:
                # Преобразуем key в более надежную форму для сравнения
                if isinstance(key, kb.Key) and key == kb.Key.caps_lock:
                    compare_key = kb.Key.caps_lock
                elif hasattr(key, '_name_') and key._name_ == self.spam_key._name_:
                    compare_key = key
                else:
                    compare_key = key
                    
                if compare_key == self.menu_key:
                    self.toggle_menu()
                
                if self.program_enabled:
                    # Сравнение для специальных клавиш
                    if isinstance(key, kb.Key) and isinstance(self.spam_key, kb.Key) and key._name_ == self.spam_key._name_:
                        self.toggle_spam()
                    elif isinstance(key, kb.Key) and isinstance(self.lmb_key, kb.Key) and key._name_ == self.lmb_key._name_:
                        self.toggle_lmb()
                    elif isinstance(key, kb.Key) and isinstance(self.custom_key, kb.Key) and key._name_ == self.custom_key._name_:
                        self.toggle_custom()
                    # Обычное сравнение для других клавиш
                    elif key == self.spam_key:
                        self.toggle_spam()
                    elif key == self.lmb_key:
                        self.toggle_lmb()
                    elif key == self.custom_key:
                        self.toggle_custom()
            except Exception as e:
                print(f"Error in keyboard listener: {e}")
            return True
        
        self.keyboard_listener = kb.Listener(on_press=on_press)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()
    
    def stop_keyboard_listener(self):
        if hasattr(self, 'keyboard_listener') and self.keyboard_listener.is_alive():
            self.keyboard_listener.stop()
    
    def restart_keyboard_listener(self):
        self.setup_keyboard_listener()
    
    def start_threads(self):
        self.stop_event = threading.Event()
        main_thread = threading.Thread(target=self.click_function, daemon=True)
        main_thread.start()
    
    def click_function(self):
        while not self.stop_event.is_set():
            if self.spam_active:
                self.keyboard.press(Key.space)
                time.sleep(0.01)
                self.keyboard.release(Key.space)
                time.sleep(0.01)
                
                self.keyboard.press('1')
                time.sleep(0.01)
                self.keyboard.release('1')
                time.sleep(0.01)
                
                self.mouse.press(Button.left)
                time.sleep(0.01)
                self.mouse.release(Button.left)
                time.sleep(0.01)

            elif self.lmb_active:
                self.mouse.press(Button.left)
                time.sleep(0.01)
                self.mouse.release(Button.left)
                time.sleep(0.01)
                
            elif self.custom_active and self.custom_sequence:
                for event in self.custom_sequence:
                    if not self.custom_active:
                        break

                    action = event.get('action')

                    if action == 'delay':
                        duration = event.get('duration', 10) / 1000
                        time.sleep(duration)
                    elif action == 'press':
                        key_type = event.get('key_type')
                        key = event.get('key')
                        if key:
                            if key_type == 'keyboard':
                                self.keyboard.press(key)
                                with self.pressed_keys_lock:
                                    self.currently_pressed_keys.add(('keyboard', key))
                            elif key_type == 'mouse':
                                self.mouse.press(key)
                                with self.pressed_keys_lock:
                                    self.currently_pressed_keys.add(('mouse', key))
                    elif action == 'release':
                        key_type = event.get('key_type')
                        key = event.get('key')
                        if key:
                            if key_type == 'keyboard':
                                self.keyboard.release(key)
                                with self.pressed_keys_lock:
                                    self.currently_pressed_keys.discard(('keyboard', key))
                            elif key_type == 'mouse':
                                self.mouse.release(key)
                                with self.pressed_keys_lock:
                                    self.currently_pressed_keys.discard(('mouse', key))
                    
                    time.sleep(0.01)
            else:
                time.sleep(0.01)
    
    def toggle_program(self):
        self.program_enabled = not self.program_enabled
        colors = self.get_colors()
        
        if self.program_enabled:
            self.program_button.configure(text="Disable Program", text_color=colors['danger'])
            self.status_label.configure(text="ACTIVE", text_color=colors['success'])
            self.status_indicator.configure(text_color=colors['success'])
        else:
            self.program_button.configure(text="Enable Program", text_color=colors['accent'])
            self.status_label.configure(text="DISABLED", text_color=colors['danger'])
            self.status_indicator.configure(text_color=colors['danger'])
            self.spam_active = False
            self.lmb_active = False
            if self.menu_visible:
                self.update_button_states()
    
    def update_button_states(self):
        colors = self.get_colors()
        
        if self.spam_active:
            self.spam_button.configure(text="Disable", text_color=colors['danger'])
            if isinstance(self.spam_button, NeumorphicButton):
                self.spam_button.set_active(True)
        else:
            self.spam_button.configure(text="Enable", text_color=colors['accent'])
            if isinstance(self.spam_button, NeumorphicButton):
                self.spam_button.set_active(False)
            
        if self.lmb_active:
            self.lmb_button.configure(text="Disable", text_color=colors['danger'])
            if isinstance(self.lmb_button, NeumorphicButton):
                self.lmb_button.set_active(True)
        else:
            self.lmb_button.configure(text="Enable", text_color=colors['accent'])
            if isinstance(self.lmb_button, NeumorphicButton):
                self.lmb_button.set_active(False)
                
        if self.custom_active:
            self.custom_button.configure(text="Disable", text_color=colors['danger'])
            if isinstance(self.custom_button, NeumorphicButton):
                self.custom_button.set_active(True)
        else:
            self.custom_button.configure(text="Enable", text_color=colors['accent'])
            if isinstance(self.custom_button, NeumorphicButton):
                self.custom_button.set_active(False)
    
    def _set_active_function(self, function_to_activate=None):
        # Deactivate all functions, releasing keys if necessary
        if self.custom_active:
            self.release_all_keys()
        self.spam_active = False
        self.lmb_active = False
        self.custom_active = False
        
        # Activate the new one
        if function_to_activate == 'spam':
            self.spam_active = True
        elif function_to_activate == 'lmb':
            self.lmb_active = True
        elif function_to_activate == 'custom':
            self.custom_active = True

        if self.menu_visible:
            self.update_button_states()
    
    def toggle_spam(self):
        new_function = None if self.spam_active else 'spam'
        self._set_active_function(new_function)
    
    def toggle_lmb(self):
        new_function = None if self.lmb_active else 'lmb'
        self._set_active_function(new_function)
    
    def toggle_menu(self):
        self.menu_visible = not self.menu_visible
        if self.menu_visible:
            self.root.attributes('-alpha', 0.0)
            self.root.deiconify()
            self.root.after(50, lambda: self.root.attributes('-alpha', 1.0))
            self.root.after(50, self.update_button_states)
        else:
            self.root.withdraw()
    
    def release_all_keys(self):
        with self.pressed_keys_lock:
            keys_to_release = list(self.currently_pressed_keys)
            for key_type, key in keys_to_release:
                try:
                    if key_type == 'keyboard':
                        self.keyboard.release(key)
                    elif key_type == 'mouse':
                        self.mouse.release(key)
                except Exception:
                    # Ignore errors, e.g., if key is already released
                    pass
            self.currently_pressed_keys.clear()
    
    def key_to_string(self, key):
        if key is None:
            return None
        if hasattr(key, '_name_'):
            return key._name_.upper()
        elif hasattr(key, 'name'):
            return key.name.upper()
        else:
            return key.char.upper()
    
    def create_dialog(self, title, message):
        self.root.attributes('-topmost', False)
        
        colors = self.get_colors()
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("360x200")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(fg_color=colors['bg'])
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        dialog_frame = NeumorphicFrame(dialog, fg_color=colors['bg'])
        dialog_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        dialog_container = ctk.CTkFrame(dialog_frame.container, fg_color="transparent")
        dialog_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            dialog_container, 
            text=title, 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=colors['text']
        )
        title_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(
            dialog_container, 
            text=message, 
            font=ctk.CTkFont(size=14),
            text_color=colors['text']
        )
        message_label.pack(pady=5)
        
        key_indicator = ctk.CTkLabel(
            dialog_container, 
            text="Waiting for key press...", 
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color=colors['accent']
        )
        key_indicator.pack(pady=10)
        
        esc_hint = ctk.CTkLabel(
            dialog_container, 
            text="Press ESC to cancel", 
            font=ctk.CTkFont(size=12),
            text_color=colors['text']
        )
        esc_hint.pack(pady=(5, 0))
        
        dialog.lift()
        dialog.focus_force()
        dialog.after(100, lambda: dialog.focus_force())
        
        return dialog, key_indicator
    
    def change_spam_bind(self):
        self.stop_keyboard_listener()
        
        dialog, indicator = self.create_dialog("Change Binding", "Press a key for the spam function")
        
        def on_key_press(key):
            listener.stop()
            colors = self.get_colors()
            if key != kb.Key.esc:
                self.spam_key = key
                self.spam_key_str = self.key_to_string(key)
                self.spam_bind_label.configure(text=self.spam_key_str)
                self.save_settings()
                self.finish_key_binding(dialog)
            else:
                indicator.configure(
                    text="Cancelled", 
                    text_color=colors['danger']
                )
                dialog.after(800, lambda: self.finish_key_binding(dialog))
            return False
        
        listener = kb.Listener(on_press=on_key_press)
        listener.start()
    
    def change_lmb_bind(self):
        self.stop_keyboard_listener()
        
        dialog, indicator = self.create_dialog("Change Binding", "Press a key for the auto-click function")
        
        def on_key_press(key):
            listener.stop()
            colors = self.get_colors()
            if key != kb.Key.esc:
                self.lmb_key = key
                self.lmb_key_str = self.key_to_string(key)
                self.lmb_bind_label.configure(text=self.lmb_key_str)
                self.save_settings()
                self.finish_key_binding(dialog)
            else:
                indicator.configure(
                    text="Cancelled", 
                    text_color=colors['danger']
                )
                dialog.after(800, lambda: self.finish_key_binding(dialog))
            return False
        
        listener = kb.Listener(on_press=on_key_press)
        listener.start()
    
    def finish_key_binding(self, dialog):
        self.close_dialog(dialog)
        self.restart_keyboard_listener()
    
    def close_dialog(self, dialog):
        dialog.grab_release()
        dialog.destroy()
        self.root.attributes('-topmost', True)
        self.root.lift()
    
    def toggle_custom(self):
        new_function = None if self.custom_active else 'custom'
        self._set_active_function(new_function)
    
    def add_custom_key(self, event_data):
        self.custom_sequence.append(event_data)
        self.save_settings()
        return len(self.custom_sequence) - 1
    
    def remove_custom_key(self, index):
        if 0 <= index < len(self.custom_sequence):
            del self.custom_sequence[index]
            self.save_settings()
            return True
        return False
    
    def update_custom_key(self, index, event_data):
        if 0 <= index < len(self.custom_sequence):
            self.custom_sequence[index] = event_data
            self.save_settings()
            return True
        return False
    
    def change_custom_bind(self):
        self.stop_keyboard_listener()
        
        dialog, indicator = self.create_dialog("Change Binding", "Press a key to activate the custom function")
        
        def on_key_press(key):
            listener.stop()
            colors = self.get_colors()
            if key != kb.Key.esc:
                self.custom_key = key
                self.custom_key_str = self.key_to_string(key)
                self.custom_bind_label.configure(text=self.custom_key_str)
                self.save_settings()
                self.finish_key_binding(dialog)
            else:
                indicator.configure(
                    text="Cancelled", 
                    text_color=colors['danger']
                )
                dialog.after(800, lambda: self.finish_key_binding(dialog))
            return False
        
        listener = kb.Listener(on_press=on_key_press)
        listener.start()
    
    def open_custom_settings(self):
        self.root.attributes('-topmost', False)
        
        colors = self.get_colors()
        
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Sequence Configuration")
        settings_window.geometry("600x540")
        settings_window.minsize(600, 540)
        settings_window.resizable(True, True)
        settings_window.attributes('-topmost', True)
        settings_window.transient(self.root)
        settings_window.grab_set()
        settings_window.configure(fg_color=colors['bg'])
        
        settings_window.update_idletasks()
        width = settings_window.winfo_width()
        height = settings_window.winfo_height()
        x = (settings_window.winfo_screenwidth() // 2) - (width // 2)
        y = (settings_window.winfo_screenheight() // 2) - (height // 2)
        settings_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        main_scroll = ctk.CTkScrollableFrame(settings_window, fg_color=colors['bg'])
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        main_frame = NeumorphicFrame(main_scroll, fg_color=colors['bg'])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        main_container = ctk.CTkFrame(main_frame.container, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        title_label = ctk.CTkLabel(
            main_container, 
            text="Custom Sequence Configuration", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=colors['text']
        )
        title_label.pack(pady=(0, 15))

        keys_frame = NeumorphicFrame(main_container, fg_color=colors['bg'])
        keys_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        keys_container = ctk.CTkFrame(keys_frame.container, fg_color="transparent")
        keys_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        header_frame = ctk.CTkFrame(keys_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        header_label = ctk.CTkLabel(
            header_frame, 
            text="Current Sequence:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors['text']
        )
        header_label.pack(side="left")
        
        sequence_frame = ctk.CTkScrollableFrame(
            keys_container,
            fg_color=colors['bg'],
            corner_radius=10,
            height=200
        )
        sequence_frame.pack(fill="x", expand=True)
        
        sequence_items = []
        
        def refresh_sequence():
            for item in sequence_items:
                item.destroy()
            sequence_items.clear()
            
            if not self.custom_sequence:
                empty_label = ctk.CTkLabel(
                    sequence_frame,
                    text="Sequence is empty. Add keys.",
                    font=ctk.CTkFont(size=14, slant="italic"),
                    text_color=colors['text']
                )
                empty_label.pack(pady=20)
                sequence_items.append(empty_label)
            else:
                for i, key_entry in enumerate(self.custom_sequence):
                    item = self.create_sequence_item(sequence_frame, i, key_entry, refresh_sequence)
                    sequence_items.append(item)
        
        refresh_sequence()
        
        actions_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        actions_frame.pack(fill="x", pady=15)
        
        add_button = NeumorphicButton(
            actions_frame,
            text="Add Key",
            font=ctk.CTkFont(size=14),
            width=160,
            height=40,
            fg_color=colors['surface'],
            text_color=colors['accent'],
            hover_color=colors['hover'],
            command=lambda: self._show_event_dialog(settings_window, callback=refresh_sequence)
        )
        add_button.pack(side="left", padx=(0, 10))
        
        clear_button = NeumorphicButton(
            actions_frame,
            text="Clear All",
            font=ctk.CTkFont(size=14),
            width=140,
            height=40,
            fg_color=colors['surface'],
            text_color=colors['danger'],
            hover_color=colors['hover'],
            command=lambda: [self.custom_sequence.clear(), refresh_sequence()]
        )
        clear_button.pack(side="left")
        
        close_button = NeumorphicButton(
            actions_frame,
            text="Close",
            font=ctk.CTkFont(size=14),
            width=120,
            height=40,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=lambda: self.close_settings_window(settings_window)
        )
        close_button.pack(side="right")
        
        help_frame = NeumorphicFrame(main_container, fg_color=colors['bg'])
        help_frame.pack(fill="x")
        
        help_container = ctk.CTkFrame(help_frame.container, fg_color="transparent")
        help_container.pack(fill="x", padx=10, pady=10)
        
        help_title = ctk.CTkLabel(
            help_container,
            text="How it works:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors['text']
        )
        help_title.pack(anchor="w", pady=(0, 5))
        
        help_text = ctk.CTkLabel(
            help_container,
            text="1. Add keys to the sequence\n" 
                 "2. Set delay between presses\n"
                 "3. Activate by pressing F3 (or change in settings)",
            font=ctk.CTkFont(size=13),
            text_color=colors['text'],
            justify="left"
        )
        help_text.pack(anchor="w")
    
    def create_sequence_item(self, parent, index, key_entry, refresh_callback=None):
        colors = self.get_colors()
        
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=5)
        
        number_label = ctk.CTkLabel(
            item_frame,
            text=f"{index+1}.",
            font=ctk.CTkFont(size=14),
            width=30,
            text_color=colors['text']
        )
        number_label.pack(side="left")

        action = key_entry.get('action', 'delay')
        info_text = ""
        if action == 'delay':
            duration = key_entry.get('duration', 10)
            info_text = f"Delay: {duration} ms"
        else:
            action_text = "Press" if action == 'press' else "Release"
            key_type = key_entry.get('key_type', 'keyboard').capitalize()
            key = key_entry.get('key')
            key_text = self.key_to_string(key) if key else "N/A"
            info_text = f"Action: {action_text} | Type: {key_type} | Key: {key_text}"

        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            text_color=colors['text'],
            justify="left"
        )
        info_label.pack(side="left", padx=10, fill="x", expand=True)
        
        edit_button = NeumorphicButton(
            item_frame,
            text="✏️",
            font=ctk.CTkFont(size=12),
            width=40,
            height=30,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=lambda: self._show_event_dialog(parent, index, refresh_callback)
        )
        edit_button.pack(side="right", padx=(0, 5))
        
        delete_button = NeumorphicButton(
            item_frame,
            text="❌",
            font=ctk.CTkFont(size=12),
            width=40,
            height=30,
            fg_color=colors['surface'],
            text_color=colors['danger'],
            hover_color=colors['hover'],
            command=lambda: [self.remove_custom_key(index), refresh_callback()]
        )
        delete_button.pack(side="right", padx=5)
        
        return item_frame
    
    def close_settings_window(self, window):
        window.grab_release()
        window.destroy()
        self.root.attributes('-topmost', True)
        self.root.lift()
    
    def _show_event_dialog(self, parent, index=None, callback=None):
        key_entry = self.custom_sequence[index] if index is not None else None
        
        colors = self.get_colors()
        
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Edit Event" if key_entry else "Add Event")
        dialog.geometry("450x400")
        dialog.minsize(450, 400)
        dialog.attributes('-topmost', True)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.configure(fg_color=colors['bg'])
        
        dialog_frame = NeumorphicFrame(dialog, fg_color=colors['bg'])
        dialog_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        dialog_container = ctk.CTkFrame(dialog_frame.container, fg_color="transparent")
        dialog_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_text = f"Edit Event #{index+1}" if key_entry else "Add New Event to Sequence"
        title_label = ctk.CTkLabel(dialog_container, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), text_color=colors['text'])
        title_label.pack(pady=(0, 15))

        # --- Define initial values and variables ---
        initial_action = "Press"
        initial_key_type = "Keyboard"
        initial_duration = "10"
        initial_key = None

        if key_entry:
            initial_action = key_entry.get('action', 'press').capitalize()
            initial_key_type = (key_entry.get('key_type') or 'keyboard').capitalize()
            initial_duration = str(key_entry.get('duration', 10))
            initial_key = key_entry.get('key')

        action_var = ctk.StringVar(value=initial_action)
        key_type_var = ctk.StringVar(value=initial_key_type)
        duration_var = ctk.StringVar(value=initial_duration)
        selected_key = {'key_type': key_type_var.get().lower(), 'key': initial_key}

        key_controls_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
        duration_controls_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
        key_select_frame = ctk.CTkFrame(key_controls_frame, fg_color="transparent")
        key_display_text = self.key_to_string(selected_key['key']) if selected_key['key'] else "<Not Selected>"
        key_display = ctk.CTkLabel(key_select_frame, text=key_display_text, font=ctk.CTkFont(size=14, weight="bold"), text_color=colors['accent'])
        mouse_keys = {"Left": Button.left, "Right": Button.right, "Middle": Button.middle}
        mouse_key_var = ctk.StringVar()
        
        # --- Define helper functions first ---
        def select_key_from_dialog():
            self.stop_keyboard_listener()
            dialog.attributes('-topmost', False)
            key_dialog, indicator = self.create_dialog("Select Key", "Press any key...")
            
            def on_key_press(key):
                nonlocal listener
                listener.stop()
                if key != kb.Key.esc:
                    selected_key['key'] = key
                    key_display.configure(text=self.key_to_string(key))
                self.finish_key_binding(key_dialog)
                dialog.attributes('-topmost', True)
                dialog.lift()
            
            listener = kb.Listener(on_press=on_key_press)
            listener.start()

        def on_mouse_key_select(choice):
            selected_key['key'] = mouse_keys[choice]
            key_display.configure(text=f"Mouse {choice}")

        def update_key_options():
            key_type = key_type_var.get().lower()
            selected_key['key_type'] = key_type
            if key_type == 'keyboard':
                mouse_key_menu.pack_forget()
                select_key_button.pack(side="left", padx=5)
                key_display.pack(side="left", padx=5)
            else: # Mouse
                select_key_button.pack_forget()
                key_display.pack_forget() # Hide old display
                mouse_key_menu.pack(side="left", padx=5)
                key_display.pack(side="left", padx=5) # Re-pack to ensure order
                on_mouse_key_select(mouse_key_var.get())

        def toggle_ui():
            action = action_var.get()
            if action == "Delay":
                key_controls_frame.pack_forget()
                duration_controls_frame.pack(fill="x", pady=10)
            else: # Press or Release
                duration_controls_frame.pack_forget()
                key_controls_frame.pack(fill="x", pady=10)
                update_key_options()

        # --- Create UI elements ---
        ctk.CTkLabel(dialog_container, text="Action:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        action_menu = ctk.CTkOptionMenu(dialog_container, variable=action_var, values=["Press", "Release", "Delay"], command=lambda v: toggle_ui())
        action_menu.pack(fill="x", pady=(0,10))
        
        # --- Key Controls ---
        ctk.CTkLabel(key_controls_frame, text="Key Type:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        key_type_menu = ctk.CTkOptionMenu(key_controls_frame, variable=key_type_var, values=["Keyboard", "Mouse"], command=lambda v: update_key_options())
        key_type_menu.pack(fill="x", pady=(0,10))
        
        key_select_frame.pack(fill="x", pady=5)
        select_key_button = NeumorphicButton(key_select_frame, text="Select Key", command=select_key_from_dialog)

        if selected_key['key'] in mouse_keys.values():
            for name, btn in mouse_keys.items():
                if btn == selected_key['key']:
                    mouse_key_var.set(name)
                    break
        else:
            mouse_key_var.set("Left")
            if key_type_var.get() == 'Mouse':
                selected_key['key'] = mouse_keys[mouse_key_var.get()]
                key_display.configure(text=f"Mouse {mouse_key_var.get()}")
                
        mouse_key_menu = ctk.CTkOptionMenu(key_select_frame, variable=mouse_key_var, values=list(mouse_keys.keys()), command=on_mouse_key_select)

        # --- Duration Controls ---
        ctk.CTkLabel(duration_controls_frame, text="Duration (ms):", font=ctk.CTkFont(size=14)).pack(side="left")
        duration_entry = ctk.CTkEntry(duration_controls_frame, textvariable=duration_var, width=100)
        duration_entry.pack(side="left", padx=5)

        toggle_ui() # Set initial state of the UI
        
        # --- Bottom buttons and save logic ---
        button_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0), side="bottom")
        
        cancel_button = NeumorphicButton(button_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side="left")
        
        def save_event():
            action = action_var.get().lower()
            event_data = {'action': action}
            
            for w in dialog_container.winfo_children():
                if isinstance(w, ctk.CTkLabel) and w.cget("text_color") == colors['danger']:
                    w.destroy()

            if action == 'delay':
                try:
                    duration = int(duration_var.get())
                    if duration < 1:
                        duration = 1
                    event_data['duration'] = duration
                except ValueError:
                    error_label = ctk.CTkLabel(dialog_container, text="Error: Duration must be a valid number.", text_color=colors['danger'])
                    error_label.pack(pady=5)
                    dialog.after(3000, error_label.destroy)
                    return
            else: # press/release
                if selected_key.get('key') is None:
                    error_label = ctk.CTkLabel(dialog_container, text="Error: A key must be selected.", text_color=colors['danger'])
                    error_label.pack(pady=5)
                    dialog.after(3000, error_label.destroy)
                    return
                event_data['key_type'] = selected_key['key_type']
                event_data['key'] = selected_key['key']
            
            if index is not None:
                self.update_custom_key(index, event_data)
            else:
                self.add_custom_key(event_data)
            
            if callback:
                callback()
            dialog.destroy()

        save_button = NeumorphicButton(button_frame, text="Save", command=save_event)
        save_button.pack(side="right")
    
    def get_config_path(self):
        if getattr(sys, 'frozen', False):
            if sys.platform.startswith('win'):
                app_dir = os.path.join(os.environ['APPDATA'], 'AutoClickerPy')
            else:
                app_dir = os.path.join(os.path.expanduser('~'), '.autoclickerpy')
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        os.makedirs(app_dir, exist_ok=True)
        
        return os.path.join(app_dir, 'autoclicker_config.json')
    
    def save_settings(self):
        config = {
            'spam_key': self.key_to_string(self.spam_key),
            'lmb_key': self.key_to_string(self.lmb_key),
            'custom_key': self.key_to_string(self.custom_key),
            'custom_sequence': []
        }
        
        for entry in self.custom_sequence:
            # New format saving
            event_entry = {
                'action': entry['action'],
                'key_type': entry.get('key_type'),
                'key': self.key_to_string(entry.get('key')) if entry.get('key') else None,
                'duration': entry.get('duration')
            }
            config['custom_sequence'].append(event_entry)
        
        try:
            with open(self.get_config_path(), 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")
    
    def load_settings(self):
        config_path = self.get_config_path()
        if not os.path.exists(config_path):
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if 'spam_key' in config:
                self.spam_key = self.string_to_key(config['spam_key'])
                self.spam_key_str = config['spam_key']
            
            if 'lmb_key' in config:
                self.lmb_key = self.string_to_key(config['lmb_key'])
                self.lmb_key_str = config['lmb_key']
            
            if 'custom_key' in config:
                self.custom_key = self.string_to_key(config['custom_key'])
                self.custom_key_str = config['custom_key']
            
            if 'custom_sequence' in config:
                self.custom_sequence = []
                for entry in config['custom_sequence']:
                    # Check if it's the new format or the old one for conversion
                    if 'action' in entry: # New format
                        key_entry = {
                            'action': entry['action'],
                            'key_type': entry.get('key_type'),
                            'key': self.string_to_key(entry.get('key')) if entry.get('key') else None,
                            'duration': entry.get('duration')
                        }
                        self.custom_sequence.append(key_entry)
                    else: # Old format, needs conversion
                        key = self.string_to_key(entry['key'])
                        key_type = entry['key_type']
                        action_type = entry.get('action_type', 'press')
                        duration = entry.get('duration', entry.get('delay', 10))

                        # 1. Press the key
                        self.custom_sequence.append({'action': 'press', 'key_type': key_type, 'key': key})

                        if action_type == 'hold':
                            # 2. If hold, the duration is a delay between press and release
                            self.custom_sequence.append({'action': 'delay', 'duration': duration})
                        
                        # 3. Release the key
                        self.custom_sequence.append({'action': 'release', 'key_type': key_type, 'key': key})

                        if action_type == 'press':
                            # 4. If press, the duration is a delay *after* the release
                            self.custom_sequence.append({'action': 'delay', 'duration': duration})
        except Exception as e:
            print(f"Ошибка при загрузке настроек: {e}")
    
    def string_to_key(self, key_str):
        if key_str is None:
            return None

        special_keys = {
            'F1': Key.f1, 'F2': Key.f2, 'F3': Key.f3, 'F4': Key.f4, 'F5': Key.f5,
            'F6': Key.f6, 'F7': Key.f7, 'F8': Key.f8, 'F9': Key.f9, 'F10': Key.f10,
            'F11': Key.f11, 'F12': Key.f12, 'ESC': Key.esc, 'ENTER': Key.enter,
            'SPACE': Key.space, 'TAB': Key.tab, 'DELETE': Key.delete,
            'HOME': Key.home, 'END': Key.end, 'PAGE_UP': Key.page_up,
            'PAGE_DOWN': Key.page_down, 'INSERT': Key.insert,
            'LEFT': Key.left, 'RIGHT': Key.right, 'UP': Key.up, 'DOWN': Key.down,
            'BACKSPACE': Key.backspace, 'CAPS_LOCK': Key.caps_lock,
            'PRINT_SCREEN': Key.print_screen, 'SCROLL_LOCK': Key.scroll_lock,
            'PAUSE': Key.pause, 'NUM_LOCK': Key.num_lock,
            'LEFT MOUSE BUTTON': Button.left, 'RIGHT MOUSE BUTTON': Button.right,
            'MIDDLE MOUSE BUTTON': Button.middle
        }
        
        if key_str in special_keys:
            return special_keys[key_str]
        
        # Проверяем альтернативные имена (с подчеркиванием)
        # Это нужно для правильной обработки ключей, сохраненных в разных форматах
        key_str_alt = key_str.replace(' ', '_')
        if key_str_alt in special_keys:
            return special_keys[key_str_alt]
            
        # Проверяем альтернативные имена (без подчеркивания)
        key_str_alt2 = key_str.replace('_', ' ')
        if key_str_alt2 in special_keys:
            return special_keys[key_str_alt2]
        
        if len(key_str) == 1:
            return kb.KeyCode.from_char(key_str.lower())
        
        return Key.f3
    
    def run(self):
        try:
            self.load_settings()
            
            self.spam_bind_label.configure(text=self.spam_key_str)
            self.lmb_bind_label.configure(text=self.lmb_key_str)
            self.custom_bind_label.configure(text=self.custom_key_str)
            
            self.root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop_event.set()

if __name__ == "__main__":
    try:
        if sys.platform.startswith('win'):
            run_as_admin()
            
        app = AutoClicker()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 