import itertools


class FloatObject:
    __id_iter = itertools.count()

    def __init__(self):
        self._id = str(next(self.__id_iter))

class FloatExpObject:
    __id_iter = itertools.count()

    def __init__(self):
        self._id = str(next(self.__id_iter))