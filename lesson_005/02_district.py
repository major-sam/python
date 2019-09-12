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
# TODO print() это упростило, спорить сложно :)
# TODO но можно и ещё проще. Вместо этих новых переменных оставьте одну
# TODO перепись_населения = комната + комната + комната
# TODO тогда и в принте останется один объект и join можно будет один раз применить
c_1_1 = sep.join(central_h1_room1)
c_1_2 = sep.join(central_h1_room2)
c_2_1 = sep.join(central_h2_room1)
c_2_2 = sep.join(central_h2_room2)
s_1_1 = sep.join(soviet_h1_room1)
s_1_2 = sep.join(soviet_h1_room2)
s_2_1 = sep.join(soviet_h2_room1)
s_2_2 = sep.join(soviet_h2_room2)
print(c_1_1, c_1_2, c_2_1, c_2_2, s_1_1, s_1_2, s_2_1, s_2_2, sep=sep)
