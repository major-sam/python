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
        if other.name == 'Water':
            return Storm().name
        elif other.name == 'Fire':
            return Lightning().name
        elif other.name == 'Earth':
            return Dust().name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Water:
    def __init__(self):
        self.name = 'Water'

    def __add__(self, other):
        if other.name == 'Air':
            return Storm().name
        elif other.name == 'Fire':
            return Vapor().name
        elif other.name == 'Earth':
            return Dirt().name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Fire:
    def __init__(self):
        self.name = 'Fire'

    def __add__(self, other):
        if other.name == 'Water':
            return Vapor().name
        elif other.name == 'Air':
            return Lightning().name
        elif other.name == 'Earth':
            return Lava().name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Earth:
    def __init__(self):
        self.name = 'Earth'

    def __add__(self, other):
        if other.name == 'Air':
            return Dust().name
        elif other.name == 'Fire':
            return Lava().name
        elif other.name == 'Water':
            return Dirt().name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Storm:
    def __init__(self):
        self.name = 'Storm'

    def __add__(self, other):
        if other.name == 'Air':
            return self.name
        elif other.name == 'Fire':
            return self.name
        elif other.name == 'Water':
            return self.name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Vapor:
    def __init__(self):
        self.name = 'Vapor'

    def __add__(self, other):
        if other.name == 'Air':
            return Water().name
        elif other.name == 'Fire':
            return self.name
        elif other.name == 'Water':
            return Water().name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Lightning:
    def __init__(self):
        self.name = 'Lightning'

    def __add__(self, other):
        if other.name == 'Air':
            return self.name
        elif other.name == 'Fire':
            return self.name
        elif other.name == 'Water':
            return self.name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Lava:
    def __init__(self):
        self.name = 'Lava'

    def __add__(self, other):
        if other.name == 'Air':
            return Earth().name
        elif other.name == 'Fire':
            return self.name
        elif other.name == 'Water':
            return Earth().name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Dust:
    def __init__(self):
        self.name = 'Dust'

    def __add__(self, other):
        if other.name == 'Air':
            return self.name
        elif other.name == 'Fire':
            return Earth().name
        elif other.name == 'Water':
            return Dirt().name
        elif other.name == 'Void':
            return Void().name
        else:
            return None

    def __str__(self):
        return self.name


class Dirt:
    def __init__(self):
        self.name = 'Dust'

    def __add__(self, other):
        if other.name == 'Air':
            return Earth().name
        elif other.name == 'Fire':
            return Earth().name
        elif other.name == 'Water':
            return Dirt().name
        elif other.name == 'Void':
            return Void().name
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
# я подозреваю, что я не понял задание.
