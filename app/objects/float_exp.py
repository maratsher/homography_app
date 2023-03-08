import imgui
from app.objects.gui_objects import FloatExpObject

class FloatExp(FloatExpObject):

    def __init__(self, label: str, height: int, width: int, valf = 0, bl = 15, formats = "%.4f", flag = 0):
        super().__init__()
        self._label = label + str(self._id)
        self._height = height
        self._width = width
        self._format = formats
        self._bl = bl
        self._flag = flag
        self._val = str(valf)
        self._valf = valf
        self._status = False

    def _preprocessing_val(self, val: str) -> float:
        try:
            val = float(val)
            return val
        except:
            self._val = str(self._valf)
            return self._valf

    def show(self):
        self._status, self._val = imgui.input_text_multiline(self._label, self._val, self._bl, self._width, self._height, flags = self._flag)
        self._valf = self._preprocessing_val(self._val)

    def get_valf(self)->float:
        return self._valf

    def set_valf(self, valf: float):
        self._valf = valf
        self._val = str(valf)
        self._status = True

    def get_status(self)-> bool:
        return self._status
        