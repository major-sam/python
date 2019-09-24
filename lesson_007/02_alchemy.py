# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())


class Air:
    def __init__(self):
        self.name = 'Air'

    def __add__(self, other):
        if isinstance(other, Water):
            return Storm()
        elif isinstance(other, Fire):
            return Lightning()
        elif isinstance(other, Earth):
            return Dust()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Water:
    def __init__(self):
        self.name = 'Water'

    def __add__(self, other):
        if isinstance(other, Air):
            return Air()
        elif isinstance(other, Fire):
            return Vapor()
        elif isinstance(other, Earth):
            return Dirt()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Fire:
    def __init__(self):
        self.name = 'Fire'

    def __add__(self, other):
        if isinstance(other, Water):
            return Vapor()
        elif isinstance(other, Air):
            return Lightning()
        elif isinstance(other, Earth):
            return Lava()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Earth:
    def __init__(self):
        self.name = 'Earth'

    def __add__(self, other):
        if isinstance(other, Air):
            return Dust()
        elif isinstance(other, Fire):
            return Lava()
        elif isinstance(other, Water):
            return Dirt()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Storm:
    def __init__(self):
        self.name = 'Storm'

    def __add__(self, other):
        if isinstance(other, Air):
            return self.name
        elif isinstance(other, Fire):
            return self.name
        elif isinstance(other, Water):
            return self.name
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Vapor:
    def __init__(self):
        self.name = 'Vapor'

    def __add__(self, other):
        if isinstance(other, Air):
            return Water()
        elif isinstance(other, Fire):
            return self.name
        elif isinstance(other, Water):
            return Water()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Lightning:
    def __init__(self):
        self.name = 'Lightning'

    def __add__(self, other):
        if isinstance(other, Air):
            return self.name
        elif isinstance(other, Fire):
            return self.name
        elif isinstance(other, Water):
            return self.name
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Lava:
    def __init__(self):
        self.name = 'Lava'

    def __add__(self, other):
        if isinstance(other, Air):
            return Earth()
        elif isinstance(other, Fire):
            return self.name
        elif isinstance(other, Water):
            return Earth()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Dust:
    def __init__(self):
        self.name = 'Dust'

    def __add__(self, other):
        if isinstance(other, Air):
            return self.name
        elif isinstance(other, Fire):
            return Earth()
        elif isinstance(other, Water):
            return Dirt()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Dirt:
    def __init__(self):
        self.name = 'Dust'

    def __add__(self, other):
        if isinstance(other, Air):
            return Earth()
        elif isinstance(other, Fire):
            return Earth()
        elif isinstance(other, Water):
            return Dirt()
        elif isinstance(other, Void):
            return Void()
        else:
            return None

    def __str__(self):
        return self.name


class Void:
    def __init__(self):
        self.name = 'Void'

    def __add__(self, other):
        return 'Void'

    def __str__(self):
        return self.name


print(Water(), '+', Air(), '=', Water() + Air())
print(Fire(), '+', Air(), '=', Fire() + Air())

print(Lightning() + Void())
# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.