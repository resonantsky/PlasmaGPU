# ui/style_loader.py
import os

def load_stylesheet(app, filename="style.qss"):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Style file '{filename}' not found.")