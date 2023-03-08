import imgui
from app.objects.gui_objects import FloatObject


class Float3(FloatObject):

    def __init__(self, label: str, formats = "%.4f", flag = 0, default_val = [0,0,0]):
        super().__init__()
        self._label = label + str(self._id)
        self._format = formats
        self._vals = default_val
        self._status = False
        self._flag = flag

    def show(self):
        self._status, self._vals = imgui.input_float3(
            self._label,
            *self._vals,
            self._format,
            self._flag
        )

    def get_vals(self):
        return self._vals
    
    def set_vals(self, vector: list):
        self._vals =  vector
        
    def get_status(self):
        return self._status