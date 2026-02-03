import sys
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtWidgets import QApplication

from .runtime import PlasmaMandelbrotViewer 
from .ui.style_loader import load_stylesheet
from colorama import init, Fore, Style

def print_plasma_banner():
    cyan = Fore.CYAN + Style.BRIGHT
    green = Fore.LIGHTGREEN_EX + Style.BRIGHT
    print(
        f"{cyan}╔═══════════════════════════════════════╗\n"
        f"{cyan}║     {green}Welcome to PlasmaMandelbrot{cyan}       ║\n"
        f"{cyan}╚═══════════════════════════════════════╝\n"
    )


def configure_surface_format():
    format = QSurfaceFormat()
    format.setDepthBufferSize(24)
    format.setSamples(16)
    format.setVersion(4, 2)
    format.setSwapInterval(1)
    QSurfaceFormat.setDefaultFormat(format)

def create_application():
    app = QApplication(sys.argv)
    load_stylesheet(app)
    return app


def launch_viewer():
    viewer = PlasmaMandelbrotViewer()
    viewer.showMaximized()
    return viewer

def run():
    configure_surface_format()
    app = create_application()
    init(autoreset=True)
    print_plasma_banner()
    viewer = launch_viewer()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
    