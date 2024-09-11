class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonList(metaclass=SingletonMeta):
    def __init__(self):
        self._list = []  # Inicializa la lista

    def add_item(self, item):
        if item not in self._list:
            self._list.append(item)

    def get_list(self):
        return self._list

    def __repr__(self):
        return f"SingletonList({self._list})"