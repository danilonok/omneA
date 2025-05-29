import ctypes
import tkinter as tk
from tkinter import simpledialog

def show_popup(popup_header: str, popup_text: str, input_popup: bool):
    """A simple popup tool that shows information to the user, provide header and text to show information to user.
    Use it if you need to show information to the user or to ask information(provide input_popup as true)"""
    
    if input_popup:
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            user_input = simpledialog.askstring(popup_header, popup_text)
            return f'User answered {user_input}'
        except:
            return 'There was an error showing popup'
    try:
        ctypes.windll.user32.MessageBoxW(0, popup_text, popup_header, 0)
        return 'Popup was shown to the user successfully'
    except:
        return 'There was an error showing popup'