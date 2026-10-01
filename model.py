import json
import os

class Model:
    # Модель хранит три числа A <= B <= C.
    A, B, C = 0, 1, 2
    MIN, MAX = 0, 100
    PATH = "value_data.json"

    def __init__(self):
        self._values = [10, 50, 90]
        self.observers = []
        self.load()

    # Логика подписки

    def attach(self, callback):
        # Новый подписчик сразу получает текущее состояние
        self.observers.append(callback)
        callback()

    def notify(self):
        for callback in self.observers:
            callback()

    # Доступ к значениям

    def get_values(self):
        # Отправляем копию, чтобы никто не мог коснуться оригинала
        return list(self._values)

    def set_value(self, index, value):
        if value < self.MIN:
            value = self.MIN
        if value > self.MAX:
            value = self.MAX

        old = list(self._values)
        self._values[index] = value

        match index:
            case self.A:
                self._values[self.B] = max(self._values[self.A], self._values[self.B])
                self._values[self.C] = max(self._values[self.B], self._values[self.C])
            case self.B:
                self._values[self.B] = max(self._values[self.B], self._values[self.A])
                self._values[self.B] = min(self._values[self.B], self._values[self.C])
            case self.C:
                self._values[self.B] = min(self._values[self.B], self._values[self.C])
                self._values[self.A] = min(self._values[self.A], self._values[self.B])

        if self._values == old:
            print("[Model] set_value(" + str(index) + ", " + str(value) + ") - без изменений")
            return

        print("[Model] set_value(" + str(index) + ", " + str(value) + ") -> " + str(self._values))
        self.save()
        self.notify()


    # Вспомогательное

    def get_min(self):
        return self.MIN

    def get_max(self):
        return self.MAX

    # Работа с памятью

    def save(self):
        with open(self.PATH, "w", encoding="utf-8") as f:
            json.dump(
                {"a": self._values[self.A],
                 "b": self._values[self.B],
                 "c": self._values[self.C]},
                f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.PATH):
            return
        try:
            with open(self.PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._values[self.A] = int(data.get("a", self._values[self.A]))
            self._values[self.B] = int(data.get("b", self._values[self.B]))
            self._values[self.C] = int(data.get("c", self._values[self.C]))
        except (OSError, ValueError):
            pass
