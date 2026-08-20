import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Control Hub v3.0")
        self.root.geometry("500x800")
        self.root.configure(bg="#181825") # Catppuccin Mocha Dark Theme

        # --- HEADER ---
        header_frame = tk.Frame(root, bg="#181825")
        header_frame.pack(pady=25)

        tk.Label(header_frame, text="VISION CONTROL", font=("Helvetica", 28, "bold"), 
                 fg="#cba6f7", bg="#181825").pack()
        
        tk.Label(header_frame, text="Modular Gesture Recognition Suite", font=("Helvetica", 10), 
                 fg="#9399b2", bg="#181825").pack()

        # --- BUTTON CONTAINER ---
        btn_frame = tk.Frame(root, bg="#181825")
        btn_frame.pack(expand=True)

        self.btn_style = {
            "font": ("Helvetica", 11, "bold"),
            "width": 32,
            "pady": 12,
            "fg": "#eff1f5",
            "cursor": "hand2",
            "bd": 0,
            "activebackground": "#313244"
        }

        # List of all 6 modules: (Display Text, Filename, Hex Color)
        modules = [
            ("🖱️  Virtual Mouse", "mouse_mode.py", "#89b4fa"),       # Blue
            ("🌐  Browser Navigation", "nav_mode.py", "#a6e3a1"),   # Green
            ("🎵  Media Controller", "media_mode.py", "#fab387"),   # Peach
            ("📊  Presentation Clicker", "ppt_mode.py", "#94e2d5"), # Teal
            ("🖥️  System Utilities", "system_mode.py", "#f38ba8"),   # Red
            ("✌️  Victory Celebration", "victory_mode.py", "#cba6f7") # Mauve
        ]

        for text, script, color in modules:
            self.add_mode(btn_frame, text, script, color)

        # --- FOOTER ---
        self.status = tk.Label(root, text="● System Ready", font=("Helvetica", 10, "bold"),
                              fg="#94e2d5", bg="#181825", pady=20)
        self.status.pack(side="bottom")

        tk.Label(root, text="Press 'Q' in Camera Window to Switch Modes", 
                 font=("Helvetica", 9), fg="#585b70", bg="#181825").pack(side="bottom")

    def add_mode(self, parent, text, script_name, color):
        btn = tk.Button(parent, text=text, bg=color, 
                        command=lambda s=script_name, t=text: self.launch(s, t), 
                        **self.btn_style)
        btn.pack(pady=8)

    def launch(self, script_name, mode_name):
        if os.path.exists(script_name):
            self.status.config(text=f"● Running {mode_name}...", fg="#f9e2af")
            try:
                # Launching as a subprocess ensures Python 3.13 executes the module
                subprocess.Popen([sys.executable, script_name])
            except Exception as e:
                messagebox.showerror("Execution Error", f"Could not launch module: {e}")
        else:
            messagebox.showerror("File Not Found", 
                                 f"The module '{script_name}' was not found in this folder.")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Center Window Logic
    window_width = 500
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = GestureApp(root)
    root.mainloop()