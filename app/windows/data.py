from typing import List

import imgui
import numpy as np

from app.window import Window
from app.objects.float3 import Float3
from app.windows.plot_window import PlotWindow

class DataWindow(Window):
    def __init__(self, pw: PlotWindow()):
        super().__init__(300,800)
        self._id = "Input and output matrices"

        self._original_coord_matrix_objects = []
        self._original_coord_matrix_label = "oс"
        self._real_coord_matrix_objects = []
        self._real_coord_matrix_label = "rс"
        self._result_matrix_objects = []
        self._result_matrix_label = "rsc"

        self.region_x = 250
        self.region_y = 180

        self._num_started_coord = 5
        self._num_coord = 0

        self._homography_matrix = np.zeros((3,3))
        self._homography_matrix_status = False

        self._pw = pw

        # init started coordinates
        self._append_coordinates(self._num_started_coord)


    def _append_coordinates(self, n = 1):
        for _ in range(n):
            self._original_coord_matrix_objects.append(Float3(self._original_coord_matrix_label))
            self._real_coord_matrix_objects.append(Float3(self._real_coord_matrix_label))
            self._result_matrix_objects.append(Float3(self._result_matrix_label))
        self._num_coord += n

    def _get_matrix_from_objects(self, objects: list) -> np.ndarray:
        m = np.zeros((self._num_coord, 3))
        for i, obj in enumerate(objects):
            for j in range(3):
                m[i][j] = obj.get_vals()[j]
        return m 

    def _set_matrix_to_objects(self, matrix: np.ndarray,objects:list):
        for i, obj in enumerate(objects):
            obj.set_vals(matrix[i])

    def _draw_content(self):
        # Original Coordinates block
        imgui.text("Original Coordinates")
        imgui.begin_child("Original Coordinates region", self.region_x, self.region_y, border=True)

        for obj in self._original_coord_matrix_objects:
            obj.show() 

        imgui.end_child()

        imgui.text("")

        # Real Coordinates block
        imgui.text("Real Coordinates")
        imgui.begin_child("Real Coordinates region", self.region_x, self.region_y, border=True)
        
        for obj in self._real_coord_matrix_objects:
            obj.show() 

        imgui.end_child()

        imgui.text("")

        # Results block
        imgui.text("Results")
        imgui.begin_child("Results region", self.region_x, self.region_y, border=True)
        
        for obj in self._result_matrix_objects:
            obj.show() 

        imgui.end_child()

        imgui.text("")

        # press Add coordinate button
        if imgui.button("Add coordinate"):
            self._append_coordinates()

        # If the original matrix has been changed
        original_changed = sum([obj.get_status() for obj in self._original_coord_matrix_objects])
        hm_changed = self._homography_matrix_status

        if original_changed or hm_changed:
            result_matrix = []
            original_matrix = self._get_matrix_from_objects(self._original_coord_matrix_objects)

            kx = np.dot(original_matrix, self._homography_matrix[0])
            ky = np.dot(original_matrix, self._homography_matrix[1])
            K = np.dot(original_matrix, self._homography_matrix[2])
            x = np.round(kx / K, self._num_coord)
            y = np.round(ky / K, self._num_coord)

            for i, j in zip(x, y):
                result_matrix.append([i,j,1])
            self._set_matrix_to_objects(result_matrix, self._result_matrix_objects)

            real_coord_matrix = self._get_matrix_from_objects(self._real_coord_matrix_objects)
            
            #plot
            rm_x = real_coord_matrix[:, 0]
            rm_y = real_coord_matrix[:, 1]
            self._pw.plot(rm_x, rm_y,x,y, self._num_coord)

    def set_homography_matrix(self, matrix: np.ndarray):
        self._homography_matrix = matrix

    def set_homography_matrix_status(self, status: bool):
        self._homography_matrix_status = status
