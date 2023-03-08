from typing import List

import imgui
from imgui import plot as implot
from array import array
import numpy as np
import scipy.spatial.distance as ds

from app.window import Window

class PlotWindow(Window):
    def __init__(self):
        super().__init__(900,600)
        self._id = "Plotting window"
        self._rm_x = array("f", [0])
        self._rm_y = array("f", [0])
        self._x = array("f", [0])
        self._y = array("f", [0])
        self._num_coord = 1
        self._plot_plane = False

    def _draw_content(self):
        implot.begin_plot("plot")
        implot.plot_scatter2("result", self._x, self._y, self._num_coord)
        implot.plot_scatter2("real coord", self._rm_x, self._rm_y, self._num_coord)

        # real plane
        if self._plot_plane:
            
            zeros = np.zeros((self._num_coord,1))
            np_rm_x = np.asarray(self._rm_x).reshape((self._num_coord, 1))
            np_rm_y = np.asarray(self._rm_y).reshape((self._num_coord, 1))
            x_min = np.min(np_rm_x)
            x_max = np.max(np_rm_x)
            y_min = np.min(np_rm_y)
            y_max = np.max(np_rm_y)
            
            real_coords = np.hstack([np_rm_x, np_rm_y, zeros])
            x0, y0, _ = real_coords[
                ds.cdist([[x_min, y_max, 0]], real_coords)[0].argsort()[0]]
            x1, y1, _ = real_coords[
                ds.cdist([[x_max, y_max, 0]], real_coords)[0].argsort()[0]]
            x2, y2, _ = real_coords[
                ds.cdist([[x_max, y_min, 0]], real_coords)[0].argsort()[0]]
            x3, y3, _ = real_coords[
                ds.cdist([[x_min, y_min, 0]], real_coords)[0].argsort()[0]]
            
            line_x = array("f", [x0, x1, x2, x3, x0])
            line_y = array("f", [y0, y1, y2, y3, y0])
            implot.plot_line2("plane for real", line_x, line_y, 5)

            # result plane
            ones = np.ones((self._num_coord,1))
            np_x = np.asarray(self._x).reshape((self._num_coord, 1))
            np_y = np.asarray(self._y).reshape((self._num_coord, 1))

            x_min = np.min(np_x)
            x_max = np.max(np_x)
            y_min = np.min(np_y)
            y_max = np.max(np_y)

            result_coord = np.hstack([np_x, np_y])

            x0, y0 = result_coord[
                ds.cdist([[x_min, y_max]], result_coord)[0].argsort()[0]]
            x1, y1 = result_coord[
                ds.cdist([[x_max, y_max]], result_coord)[0].argsort()[0]]
            x2, y2 = result_coord[
                ds.cdist([[x_max, y_min]], result_coord)[0].argsort()[0]]
            x3, y3 = result_coord[
                ds.cdist([[x_min, y_min]], result_coord)[0].argsort()[0]]

            line_x = array("f", [x0, x1, x2, x3, x0])
            line_y = array("f", [y0, y1, y2, y3, y0])
            implot.plot_line2("plane for result", line_x, line_y, 5)

        implot.end_plot()

    def plot(self, rm_x, rm_y, x, y, num_coord):
        self._rm_x = array("f", rm_x)
        self._rm_y = array("f", rm_y)
        self._x = array("f", x)
        self._y = array("f", y)
        self._num_coord = num_coord
        self._plot_plane = True