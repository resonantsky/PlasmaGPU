import sys
import numpy as np
import os
os.environ['PYOPENCL_CTX'] = '0'
import pyopencl as cl
import os
import shutil
import glfw
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import OpenGL.GL as gl
from .render_fractal import render_fractal
from .mode_switch import reset_view
from .get_kernel_args import get_kernel_args
from .events import mousePressEvent, mouseReleaseEvent, mouseMoveEvent, wheelEvent



class FractalGLWidget(QOpenGLWidget):
    
    def __init__(self, runtime, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.parent_viewer = parent
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.runtime = runtime
        self.mousePressEvent = lambda event: mousePressEvent(self.runtime, event)
        self.mouseReleaseEvent = lambda event: mouseReleaseEvent(self.runtime, event)
        self.mouseMoveEvent = lambda event: mouseMoveEvent(self.runtime, event)
        self.wheelEvent = lambda event: wheelEvent(self.runtime, event)

        screen = self.screen() or self.window().screen()
        self.width = screen.size().width()
        self.height = screen.size().height()

        # Respect explicit resolution
        self.fractal_image = QImage(self.width, self.height, QImage.Format.Format_RGBA8888)

        self.texture_id = None
        self.fractal_mode = 0
        self.kernel_name = "mandelbrot_kernel"
        self.kernel_path = "mandelbrot.cl"

    def set_fractal_image(self, image: QImage):
        self.fractal_image = image
        self.update()

    def initializeGL(self):
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.texture_id = gl.glGenTextures(1)

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        if self.fractal_image is None:
            return
        img = self.fractal_image.convertToFormat(QImage.Format.Format_RGBA8888)
        w, h = img.width(), img.height()
        ptr = img.bits()
        ptr.setsize(img.sizeInBytes())
        data = ptr.asstring(img.sizeInBytes())

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        gl.glBegin(gl.GL_QUADS)
        for (tx, ty), (vx, vy) in [((0, 1), (-1, -1)), ((1, 1), (1, -1)), ((1, 0), (1, 1)), ((0, 0), (-1, 1))]:
            gl.glTexCoord2f(tx, ty)
            gl.glVertex2f(vx, vy)
        gl.glEnd()

    def compile_kernel(self):
        kernel_dir = os.path.join(os.path.dirname(__file__), '..', 'math')
        kernel_path = os.path.normpath(os.path.join(kernel_dir, self.kernel_path))

        with open(kernel_path, 'r') as f:
            kernel_source = f.read()

        self.program = cl.Program(self.runtime.context, kernel_source).build()

    def change_fractal_mode(self, index):
        self.fractal_mode = index
        self.julia_mode = (index == 1)

        self.kernel_path = {
            0: "mandelbrot.cl",
            1: "julia.cl",
            2: "newton.cl",
            3: "phoenix.cl"
        }[index]

        self.kernel_name = {
            0: "mandelbrot_kernel",
            1: "julia_kernel",
            2: "newton_kernel",
            3: "phoenix_kernel"
        }[index]

        self.offset_presets = {
            0: (0.0, 0.0),
            1: (-0.8, 0.156),
            2: (0.75, -0.0),
            3: (1.0, 0.0)
        }

        z_real, z_imag = self.offset_presets.get(index, (0.0, 0.0))
        self.runtime.z_real_offset = z_real
        self.runtime.z_imag_offset = z_imag

        print("Syncing spinboxes to:", z_real, z_imag)
        print("Actual QImage size:", self.fractal_image.width(), self.fractal_image.height())

        if hasattr(self, "parent_viewer"):
            viewer = self.parent_viewer
            viewer.z_real_offset = z_real
            viewer.z_imag_offset = z_imag
            viewer.sync_offset_controls(z_real, z_imag)

        self.compile_kernel()
        reset_view(self.runtime)
        render_fractal(self.runtime)



