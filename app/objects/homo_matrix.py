import imgui
from app.objects.float_exp import FloatExp
import numpy as np

class HomoMatrix:

    def __init__(self, label = "", height = 100, width = 100, shape = (3,3)):
        self._cells = []
        self._n = shape[0]*shape[1]
        self._label = label
        self._height = height
        self._width = width
        self._shape = shape
        self._flag = imgui.INPUT_TEXT_AUTO_SELECT_ALL

        self.init_cells()

    def init_cells(self):
        for i in range(self._shape[0]):
            self._cells.append([])
            for j in range(self._shape[1]):
                self._cells[i].append(FloatExp(self._label, self._height, self._width, flag=self._flag))

    def show(self):
        for row in self._cells:
            imgui.begin_group()
            for cell in row:
                cell.show()
                imgui.same_line(spacing=15)
            imgui.end_group()

    def get_homography_matrix(self) -> np.ndarray:
        hm = np.zeros(self._shape)
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                hm[i][j] = self._cells[i][j].get_valf()
        return hm

    def get_homography_matrix_status(self) -> bool:
        s = False
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                s += self._cells[i][j].get_status()
        return s

    def set_homography_matrix(self, matrix: np.ndarray):
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                self._cells[i][j].set_valf(matrix[i][j])

    def set_shifts(self, matrix: np.ndarray, shift_matrix: np.ndarray):
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                self._cells[i][j].set_valf( matrix[i][j] + shift_matrix[i][j] )
