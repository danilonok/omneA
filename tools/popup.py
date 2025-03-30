import ctypes

def show_popup(popup_header: str, popup_text: str):
    """A simple popup tool that shows information to the user, provide header and text to show information to user.
    Use it if you need to show information to the user"""
    try:
        ctypes.windll.user32.MessageBoxW(0, popup_text, popup_header, 0)
        return 'Popup was shown to the user successfully'
    except:
        return 'There was an error showing popup'