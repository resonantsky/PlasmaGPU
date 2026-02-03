import sys
import os
import shutil
import numpy as np

# OpenCL setup
os.environ['PYOPENCL_CTX'] = '0'

import pyopencl as cl

# Input and UI dependencies
import glfw
from PyQt6.QtCore import Qt, QTimer, QElapsedTimer
from PyQt6.QtGui import QImage, QSurfaceFormat, QIntValidator
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox,
    QPushButton, QSpinBox, QCheckBox, QLineEdit, QDoubleSpinBox, QLabel
)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import OpenGL.GL as gl

# Internal modules
from runtime.fractal_gl import FractalGLWidget
from runtime import PlasmaMandelbrotViewer

# Public API exposure
__all__ = [
    "FractalGLWidget",
    "PlasmaMandelbrotViewer",
    
]