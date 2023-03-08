from typing import List

import imgui
import numpy as np

from app.window import Window
from app.windows.data import DataWindow
from app.objects.homo_matrix import HomoMatrix


class HomographyWindow(Window):
    def __init__(self, data_window: DataWindow):
        super().__init__(900,300)
        self._id = "Homography Matrix"
        self._N = 1
        self._shape = (3,3)
        self._matrix = np.zeros(self._shape)
        self._shifts = np.zeros(self._shape)
        self._data_window = data_window

        self.hm = HomoMatrix(shape = self._shape, height=25, width=190)

    def _draw_content(self):
        imgui.text("Homography Matrix")
        self.hm.show()

        s1, self._shifts[0] = imgui.slider_float3(
            "s1", *self._shifts[0],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        s2, self._shifts[1] = imgui.slider_float3(
            "s2", *self._shifts[1],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        s3, self._shifts[2] = imgui.slider_float3(
            "s3", *self._shifts[2],
            min_value=-self._N, max_value=self._N,
            format="%.2f")

        imgui.begin_group()
        if imgui.button("Применить"):
            self._matrix = self.hm.get_homography_matrix()
            self._shifts = np.zeros((3,3))
        imgui.end_group()

        imgui.same_line(spacing=5)

        imgui.begin_group()
        if imgui.button("Сбросить"):
            self.hm.set_homography_matrix(self._matrix)
            self._shifts = np.zeros((3,3))
        imgui.end_group()

        #self._matrix = self.hm.get_homography_matrix()

        if s1 or s2 or s3:
            self.hm.set_shifts(self._matrix, self._shifts)
            s1 = s2 = s3 = False
        
        self._data_window.set_homography_matrix(self.hm.get_homography_matrix())
        self._data_window.set_homography_matrix_status(self.hm.get_homography_matrix_status())

        # imgui.text('You wrote: %' + str(list(self._matrix)))

    def get_matrix(self):
        return self._matrix

    def set_matrix(self, matrix: np.ndarray):
        self._matrix = matrix

    def set_N(self, N: float):
        self._N = N

