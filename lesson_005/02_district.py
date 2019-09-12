# -*- coding: utf-8 -*-

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join

from lesson_005.district.central_street.house1.room1 import folks as central_h1_room1
from lesson_005.district.central_street.house1.room2 import folks as central_h1_room2
from lesson_005.district.central_street.house2.room1 import folks as central_h2_room1
from lesson_005.district.central_street.house2.room2 import folks as central_h2_room2
from lesson_005.district.soviet_street.house1.room1 import folks as soviet_h1_room1
from lesson_005.district.soviet_street.house1.room2 import folks as soviet_h1_room2
from lesson_005.district.soviet_street.house2.room1 import folks as soviet_h2_room1
from lesson_005.district.soviet_street.house2.room2 import folks as soviet_h2_room2

sep = ', '
distinct_people = sep.join(
    central_h1_room1 + central_h1_room2 + central_h2_room1 +
    central_h2_room2 + soviet_h1_room1 + soviet_h1_room2 +
    soviet_h2_room1 + soviet_h2_room2)
print(distinct_people)
