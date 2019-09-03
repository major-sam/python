#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть строка с перечислением фильмов
my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

# Выведите на консоль с помощью индексации строки, последовательно:
#   первый фильм
#   последний
#   второй
#   второй с конца

# Запятая не должна выводиться.  Переопределять my_favorite_movies нельзя
# Использовать .split() или .find()или другие методы строки нельзя - пользуйтесь только срезами,
# как указано в задании!

print(my_favorite_movies[0:10])
print(my_favorite_movies[len(my_favorite_movies) - 15:len(my_favorite_movies)])  # TODO не корректная запись
print(my_favorite_movies[12:25])
print(my_favorite_movies[len(my_favorite_movies) - 22:len(my_favorite_movies) - 17])  # TODO и здесь
# TODO в обоих этих случаях лучше использовать срезы типа [-15:],
# TODO они будут идентичны срезу [len(my_favorite_movies)-15:len(my_favorite_movies)]
# TODO Кроме того, если используете что-то длинное вроде "len(my_favorite_movies)",
# TODO лучше вынести это в короткую переменную
