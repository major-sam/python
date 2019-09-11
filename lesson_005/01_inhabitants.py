# -*- coding: utf-8 -*-

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...
import os
from lesson_005.room_1 import folks as room1_folks
from lesson_005.room_2 import folks as room2_folks

sep = ', '
print('В комнате room_1 живут:', sep.join(room1_folks))
print('В комнате room_2 живут:', sep.join(room2_folks))