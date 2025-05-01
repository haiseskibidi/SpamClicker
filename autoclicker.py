import sys
import time
import threading
import ctypes
import pyautogui
import customtkinter as ctk
import json
import os
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
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.spam_active = False
        self.lmb_active = False
        self.custom_active = False
        self.menu_visible = True
        self.program_enabled = True
        
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
        self.root.resizable(False, False)
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
        
        content_frame = ctk.CTkFrame(main_frame, fg_color=colors['bg'], corner_radius=0)
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
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
                if key == self.menu_key:
                    self.toggle_menu()
                
                if self.program_enabled:
                    if key == self.spam_key:
                        self.toggle_spam()
                    elif key == self.lmb_key:
                        self.toggle_lmb()
                    elif key == self.custom_key:
                        self.toggle_custom()
            except:
                pass
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
            if not self.program_enabled:
                time.sleep(0.01)
                continue
                
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
                for key_entry in self.custom_sequence:
                    key_type = key_entry['key_type']
                    key = key_entry['key']
                    delay = key_entry['delay'] / 1000
                    
                    if key_type == 'keyboard':
                        self.keyboard.press(key)
                        time.sleep(0.01)
                        self.keyboard.release(key)
                    elif key_type == 'mouse':
                        self.mouse.press(key)
                        time.sleep(0.01)
                        self.mouse.release(key)
                    
                    time.sleep(delay)
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
    
    def toggle_spam(self):
        self.spam_active = not self.spam_active
        if self.spam_active:
            self.lmb_active = False
        
        if self.menu_visible:
            self.update_button_states()
    
    def toggle_lmb(self):
        self.lmb_active = not self.lmb_active
        if self.lmb_active:
            self.spam_active = False
        
        if self.menu_visible:
            self.update_button_states()
    
    def toggle_menu(self):
        self.menu_visible = not self.menu_visible
        if self.menu_visible:
            self.root.attributes('-alpha', 0.0)
            self.root.deiconify()
            self.root.after(50, lambda: self.root.attributes('-alpha', 1.0))
            self.root.after(50, self.update_button_states)
        else:
            self.root.withdraw()
    
    def key_to_string(self, key):
        if hasattr(key, '_name_'):
            return key._name_.upper()
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
                # Сохраняем настройки после изменения бинда
                self.save_settings()
                # Закрываем диалог без задержки
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
                # Сохраняем настройки после изменения бинда
                self.save_settings()
                # Закрываем диалог без задержки
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
        self.custom_active = not self.custom_active
        if self.custom_active:
            self.spam_active = False
            self.lmb_active = False
        
        if self.menu_visible:
            self.update_button_states()
    
    def add_custom_key(self, key_type, key, delay=10):
        key_entry = {
            'key_type': key_type,
            'key': key,
            'delay': delay
        }
        self.custom_sequence.append(key_entry)
        self.save_settings()
        return len(self.custom_sequence) - 1
    
    def remove_custom_key(self, index):
        if 0 <= index < len(self.custom_sequence):
            del self.custom_sequence[index]
            self.save_settings()
            return True
        return False
    
    def update_custom_key(self, index, key_type=None, key=None, delay=None):
        if 0 <= index < len(self.custom_sequence):
            if key_type is not None:
                self.custom_sequence[index]['key_type'] = key_type
            if key is not None:
                self.custom_sequence[index]['key'] = key
            if delay is not None:
                self.custom_sequence[index]['delay'] = delay
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
                # Сохраняем настройки после изменения бинда
                self.save_settings()
                # Закрываем диалог без задержки
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
        settings_window.resizable(False, False)
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
        
        main_frame = NeumorphicFrame(settings_window, fg_color=colors['bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
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
            command=lambda: self.add_key_dialog(settings_window, refresh_sequence)
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
        
        key_type = key_entry['key_type']
        key_type_text = "Keyboard" if key_type == 'keyboard' else "Mouse"
        key_type_label = ctk.CTkLabel(
            item_frame,
            text=key_type_text,
            font=ctk.CTkFont(size=14),
            width=100,
            text_color=colors['accent']
        )
        key_type_label.pack(side="left", padx=5)
        
        key = key_entry['key']
        key_text = key.char if hasattr(key, 'char') else key._name_ if hasattr(key, '_name_') else str(key)
        key_label = ctk.CTkLabel(
            item_frame,
            text=key_text.upper(),
            font=ctk.CTkFont(size=14, weight="bold"),
            width=80,
            text_color=colors['text']
        )
        key_label.pack(side="left", padx=5)
        
        delay_label = ctk.CTkLabel(
            item_frame,
            text=f"Delay: {key_entry['delay']} ms",
            font=ctk.CTkFont(size=14),
            width=120,
            text_color=colors['text']
        )
        delay_label.pack(side="left", padx=5)
        
        edit_button = NeumorphicButton(
            item_frame,
            text="✏️",
            font=ctk.CTkFont(size=12),
            width=40,
            height=30,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=lambda: self.edit_key_dialog(parent.winfo_toplevel(), index, refresh_callback)
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
    
    def add_key_dialog(self, parent, callback=None):
        colors = self.get_colors()
        
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Add Key")
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        dialog.transient(parent)
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
            text="Add Key", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=colors['text']
        )
        title_label.pack(pady=(0, 15))
        
        key_type_var = ctk.StringVar(value="keyboard")
        
        radio_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
        radio_frame.pack(fill="x", pady=5)
        
        keyboard_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Keyboard",
            variable=key_type_var,
            value="keyboard",
            font=ctk.CTkFont(size=14),
            fg_color=colors['accent'],
            text_color=colors['text']
        )
        keyboard_radio.pack(anchor="w", pady=2)
        
        mouse_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Mouse",
            variable=key_type_var,
            value="mouse",
            font=ctk.CTkFont(size=14),
            fg_color=colors['accent'],
            text_color=colors['text']
        )
        mouse_radio.pack(anchor="w", pady=2)
        
        mouse_options_frame = ctk.CTkFrame(radio_frame, fg_color="transparent")
        mouse_options_frame.pack(fill="x", padx=(20, 0), pady=(0, 5))
        
        mouse_button_var = ctk.StringVar(value="left")
        mouse_options_label = ctk.CTkLabel(
            mouse_options_frame,
            text="Mouse Button:",
            font=ctk.CTkFont(size=13),
            text_color=colors['text'],
            width=100
        )
        mouse_options_label.pack(side="left", padx=(0, 5))
        
        mouse_options = ctk.CTkOptionMenu(
            mouse_options_frame,
            values=["LMB", "RMB", "Wheel"],
            font=ctk.CTkFont(size=13),
            variable=mouse_button_var,
            dropdown_font=ctk.CTkFont(size=13),
            fg_color=colors['surface'],
            button_color=colors['surface'],
            button_hover_color=colors['hover'],
            dropdown_fg_color=colors['surface'],
            text_color=colors['text']
        )
        mouse_options.pack(side="left", fill="x", expand=True)
        mouse_options.set("LMB")
        
        key_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
        key_frame.pack(fill="x", pady=15)
        
        key_label = ctk.CTkLabel(
            key_frame, 
            text="Key:", 
            font=ctk.CTkFont(size=14),
            text_color=colors['text'],
            width=80
        )
        key_label.pack(side="left")
        
        key_value_label = ctk.CTkLabel(
            key_frame, 
            text="Not selected", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors['accent']
        )
        key_value_label.pack(side="left", padx=10)
        
        select_key_button = NeumorphicButton(
            key_frame,
            text="Select",
            font=ctk.CTkFont(size=14),
            width=100,
            height=30,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=lambda: select_key()
        )
        select_key_button.pack(side="right")
        
        selected_key = {'key': None, 'key_type': None}
        
        def update_key_visibility(*args):
            key_type = key_type_var.get()
            
            if key_type == "mouse":
                mouse_options_frame.pack(fill="x", padx=(20, 0), pady=(0, 5))
                mouse_button = mouse_button_var.get()
                from pynput.mouse import Button
                
                if mouse_button == "LMB":
                    selected_key['key'] = Button.left
                    key_value_label.configure(text="LEFT MOUSE BUTTON")
                elif mouse_button == "RMB":
                    selected_key['key'] = Button.right
                    key_value_label.configure(text="RIGHT MOUSE BUTTON")
                elif mouse_button == "Wheel":
                    selected_key['key'] = Button.middle
                    key_value_label.configure(text="MIDDLE MOUSE BUTTON (WHEEL)")
                
                selected_key['key_type'] = 'mouse'
                key_frame.pack(fill="x", pady=15)
                select_key_button.configure(state="disabled")
            else:
                mouse_options_frame.pack_forget()
                
                if key_type == "keyboard":
                    key_frame.pack(fill="x", pady=15)
                    key_value_label.configure(text="Not selected")
                    select_key_button.configure(state="normal")
                    selected_key['key'] = None
                    selected_key['key_type'] = None
        
        key_type_var.trace_add("write", update_key_visibility)
        mouse_button_var.trace_add("write", update_key_visibility)
        
        update_key_visibility()
        
        def select_key():
            nonlocal selected_key
            key_type = key_type_var.get()
            
            if key_type != "keyboard":
                return
            
            select_key_button.configure(state="disabled")
            keyboard_radio.configure(state="disabled")
            mouse_radio.configure(state="disabled")
            mouse_options.configure(state="disabled")
            
            key_indicator = ctk.CTkLabel(
                dialog_container, 
                text="Press a key...", 
                font=ctk.CTkFont(size=14, slant="italic"),
                text_color=colors['accent']
            )
            key_indicator.pack(pady=10)
            
            def on_key_press(key):
                nonlocal selected_key
                listener.stop()
                
                selected_key = {'key': key, 'key_type': 'keyboard'}
                key_text = key.char if hasattr(key, 'char') else key._name_ if hasattr(key, '_name_') else str(key)
                key_value_label.configure(text=key_text.upper())
                
                select_key_button.configure(state="normal")
                keyboard_radio.configure(state="normal")
                mouse_radio.configure(state="normal")
                mouse_options.configure(state="normal")
                
                key_indicator.destroy()
                return False
            
            listener = kb.Listener(on_press=on_key_press)
            listener.start()
        
        delay_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
        delay_frame.pack(fill="x", pady=15)
        
        delay_label = ctk.CTkLabel(
            delay_frame, 
            text="Delay (ms):", 
            font=ctk.CTkFont(size=14),
            text_color=colors['text'],
            width=120
        )
        delay_label.pack(side="left")
        
        delay_entry = ctk.CTkEntry(
            delay_frame,
            font=ctk.CTkFont(size=14),
            width=100,
            justify="right",
            placeholder_text="10"
        )
        delay_entry.pack(side="left", padx=10)
        delay_entry.insert(0, "10")
        
        ms_label = ctk.CTkLabel(
            delay_frame, 
            text="ms", 
            font=ctk.CTkFont(size=14),
            text_color=colors['text']
        )
        ms_label.pack(side="left")
        
        button_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0), side="bottom")
        
        cancel_button = NeumorphicButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            width=100,
            height=35,
            fg_color=colors['surface'],
            text_color=colors['text'],
            hover_color=colors['hover'],
            command=lambda: dialog.destroy()
        )
        cancel_button.pack(side="left")
        
        save_button = NeumorphicButton(
            button_frame,
            text="Save",
            font=ctk.CTkFont(size=14),
            width=100,
            height=35,
            fg_color=colors['surface'],
            text_color=colors['accent'],
            hover_color=colors['hover'],
            command=lambda: save_key()
        )
        save_button.pack(side="right")
        
        def save_key():
            try:
                if selected_key['key'] is None:
                    error_label = ctk.CTkLabel(
                        dialog_container, 
                        text="Error: Select a key!", 
                        font=ctk.CTkFont(size=14),
                        text_color=colors['danger']
                    )
                    error_label.pack(pady=5)
                    dialog.after(2000, error_label.destroy)
                    return
                
                delay = int(delay_entry.get())
                if delay < 1:
                    delay = 10
                
                self.add_custom_key(
                    key_type=selected_key['key_type'],
                    key=selected_key['key'],
                    delay=delay
                )
                
                dialog.destroy()
                if callback:
                    callback()
            except ValueError:
                error_label = ctk.CTkLabel(
                    dialog_container, 
                    text="Error: Enter a valid number for delay!", 
                    font=ctk.CTkFont(size=14),
                    text_color=colors['danger']
                )
                error_label.pack(pady=5)
                dialog.after(2000, error_label.destroy)
    
    def edit_key_dialog(self, parent, index, callback=None):
        if 0 <= index < len(self.custom_sequence):
            key_entry = self.custom_sequence[index]
            colors = self.get_colors()
            
            dialog = ctk.CTkToplevel(parent)
            dialog.title("Edit Key")
            dialog.geometry("400x300")
            dialog.resizable(False, False)
            dialog.attributes('-topmost', True)
            dialog.transient(parent)
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
                text=f"Edit Key #{index+1}", 
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=colors['text']
            )
            title_label.pack(pady=(0, 15))
            
            delay_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
            delay_frame.pack(fill="x", pady=15)
            
            delay_label = ctk.CTkLabel(
                delay_frame, 
                text="Delay (ms):", 
                font=ctk.CTkFont(size=14),
                text_color=colors['text'],
                width=120
            )
            delay_label.pack(side="left")
            
            delay_entry = ctk.CTkEntry(
                delay_frame,
                font=ctk.CTkFont(size=14),
                width=100,
                justify="right"
            )
            delay_entry.pack(side="left", padx=10)
            delay_entry.insert(0, str(key_entry['delay']))
            
            ms_label = ctk.CTkLabel(
                delay_frame, 
                text="ms", 
                font=ctk.CTkFont(size=14),
                text_color=colors['text']
            )
            ms_label.pack(side="left")
            
            info_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
            info_frame.pack(fill="x", pady=15)
            
            key_type = key_entry['key_type']
            key_type_text = "Keyboard" if key_type == 'keyboard' else "Mouse"
            
            key = key_entry['key']
            key_text = key.char if hasattr(key, 'char') else key._name_ if hasattr(key, '_name_') else str(key)
            
            info_label = ctk.CTkLabel(
                info_frame, 
                text=f"Type: {key_type_text}\nKey: {key_text.upper()}", 
                font=ctk.CTkFont(size=14),
                text_color=colors['text'],
                justify="left"
            )
            info_label.pack(anchor="w")
            
            note_label = ctk.CTkLabel(
                dialog_container, 
                text="Note: To change the key, delete this one and add a new one.", 
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color=colors['text']
            )
            note_label.pack(pady=10)
            
            button_frame = ctk.CTkFrame(dialog_container, fg_color="transparent")
            button_frame.pack(fill="x", pady=(20, 0), side="bottom")
            
            cancel_button = NeumorphicButton(
                button_frame,
                text="Cancel",
                font=ctk.CTkFont(size=14),
                width=100,
                height=35,
                fg_color=colors['surface'],
                text_color=colors['text'],
                hover_color=colors['hover'],
                command=lambda: dialog.destroy()
            )
            cancel_button.pack(side="left")
            
            save_button = NeumorphicButton(
                button_frame,
                text="Save",
                font=ctk.CTkFont(size=14),
                width=100,
                height=35,
                fg_color=colors['surface'],
                text_color=colors['accent'],
                hover_color=colors['hover'],
                command=lambda: save_key()
            )
            save_button.pack(side="right")
            
            def save_key():
                try:
                    delay = int(delay_entry.get())
                    if delay < 1:
                        delay = 10
                    
                    self.update_custom_key(index, delay=delay)
                    
                    dialog.destroy()
                    if callback:
                        callback()
                except ValueError:
                    error_label = ctk.CTkLabel(
                        dialog_container, 
                        text="Error: Enter a valid number for delay!", 
                        font=ctk.CTkFont(size=14),
                        text_color=colors['danger']
                    )
                    error_label.pack(pady=5)
                    dialog.after(2000, error_label.destroy)
    
    def get_config_path(self):
        """Получает путь к файлу конфигурации."""
        app_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(app_dir, 'autoclicker_config.json')
    
    def save_settings(self):
        """Сохраняет настройки в JSON-файл."""
        config = {
            'spam_key': self.key_to_string(self.spam_key),
            'lmb_key': self.key_to_string(self.lmb_key),
            'custom_key': self.key_to_string(self.custom_key),
            'custom_sequence': []
        }
        
        # Сохраняем кастомную последовательность
        for entry in self.custom_sequence:
            key_entry = {
                'key_type': entry['key_type'],
                'key': self.key_to_string(entry['key']),
                'delay': entry['delay']
            }
            config['custom_sequence'].append(key_entry)
        
        try:
            with open(self.get_config_path(), 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")
    
    def load_settings(self):
        """Загружает настройки из JSON-файла."""
        config_path = self.get_config_path()
        if not os.path.exists(config_path):
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Загружаем настройки клавиш
            if 'spam_key' in config:
                self.spam_key = self.string_to_key(config['spam_key'])
                self.spam_key_str = config['spam_key']
            
            if 'lmb_key' in config:
                self.lmb_key = self.string_to_key(config['lmb_key'])
                self.lmb_key_str = config['lmb_key']
            
            if 'custom_key' in config:
                self.custom_key = self.string_to_key(config['custom_key'])
                self.custom_key_str = config['custom_key']
            
            # Загружаем кастомную последовательность
            if 'custom_sequence' in config:
                self.custom_sequence = []
                for entry in config['custom_sequence']:
                    key_entry = {
                        'key_type': entry['key_type'],
                        'key': self.string_to_key(entry['key']),
                        'delay': entry['delay']
                    }
                    self.custom_sequence.append(key_entry)
        except Exception as e:
            print(f"Ошибка при загрузке настроек: {e}")
    
    def string_to_key(self, key_str):
        """Преобразует строковое представление клавиши в объект Key."""
        # Обработка специальных клавиш
        special_keys = {
            'F1': Key.f1, 'F2': Key.f2, 'F3': Key.f3, 'F4': Key.f4, 'F5': Key.f5,
            'F6': Key.f6, 'F7': Key.f7, 'F8': Key.f8, 'F9': Key.f9, 'F10': Key.f10,
            'F11': Key.f11, 'F12': Key.f12, 'ESC': Key.esc, 'ENTER': Key.enter,
            'SPACE': Key.space, 'TAB': Key.tab, 'DELETE': Key.delete,
            'HOME': Key.home, 'END': Key.end, 'PAGE UP': Key.page_up,
            'PAGE DOWN': Key.page_down, 'INSERT': Key.insert,
            'LEFT': Key.left, 'RIGHT': Key.right, 'UP': Key.up, 'DOWN': Key.down,
            'BACKSPACE': Key.backspace, 'CAPS LOCK': Key.caps_lock,
            'PRINT SCREEN': Key.print_screen, 'SCROLL LOCK': Key.scroll_lock,
            'PAUSE': Key.pause, 'NUM LOCK': Key.num_lock,
            'LEFT MOUSE BUTTON': Button.left, 'RIGHT MOUSE BUTTON': Button.right,
            'MIDDLE MOUSE BUTTON': Button.middle
        }
        
        if key_str in special_keys:
            return special_keys[key_str]
        
        # Обработка обычных символов
        if len(key_str) == 1:
            return kb.KeyCode.from_char(key_str.lower())
        
        return Key.f3  # По умолчанию возвращаем F3, если не удалось распознать
    
    def run(self):
        try:
            # Загружаем настройки перед запуском приложения
            self.load_settings()
            
            # Обновляем метки на интерфейсе с загруженными настройками
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