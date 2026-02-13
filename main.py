from gui.app import App
import customtkinter as ctk
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
