# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
    return prime_numbers


# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:

    def __init__(self, n):
        self.num = 1
        self.end = n
        self.list = []

    def __iter__(self):
        return self

    def __next__(self):
        self.num += 1
        self.res = None
        if self.num < self.end:
            if self.is_prime(self.num, self.list):
                self.list.append(self.num)
                self.res = self.num
            if self.res is None:
                return next(self)
            else:
                return self.res
        else:
            raise StopIteration()

    def is_prime(self, num, arr):
        for element in arr:
            if num % element == 0:
                return False
        return True


#
# prime_number_iterator = PrimeNumbers(n=10000)
# for number in prime_number_iterator:
#     print(number)


# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def numbers_generator(n):
    prime_numbers = []
    mersenn_number = 2
    for generator_number in range(2, n + 1):
        generator_state = check_number(generator_number, prime_numbers, mersenn_number)
        if "prime" in generator_state:
            prime_numbers.append(generator_number)
        if "Marsenn" in generator_state:
            mersenn_number += 1
        if generator_state != "":
            yield generator_number, generator_state


def check_number(_number, prime_numbers, mersenn):
    _state = ""
    num_as_list = [int(x) for x in str(_number)]
    if is_prime(_number, prime_numbers):
        _state = _state + " is prime"
    if is_lucky(num_as_list):
        if _state != "":
            _state = _state + " and lucky"
        else:
            _state = " is lucky"
    if is_marsenns(_number, mersenn):
        if _state != "":
            _state = _state + " and Marsenn"
        else:
            _state = _state + " is Marsenn"
    if is_palindrom(num_as_list):
        _state = _state + " and palindrom"
    return _state


def is_prime(_number, prime_numbers):
    for prime in prime_numbers:
        if _number % prime == 0:
            return False
    else:
        return True


def is_marsenns(_number, mersenn):  # https://clck.ru/K6f2w
    if _number == 2 ** mersenn - 1:
        return True
    else:
        return False


def is_lucky(_num_list):
    int_len = len(_num_list)
    if int_len > 1:
        left_num_list, right_num_list = [], []
        buffer = 0
        nums = int_len // 2
        while buffer < nums:
            # print(num_list[buffer], "<>", num_list[int_len - 1 - buffer])
            left_num_list.append(_num_list[buffer])
            right_num_list.append(_num_list[int_len - 1 - buffer])
            buffer += 1
        left_num = summarization(left_num_list)
        right_num = summarization(right_num_list)
        # print(left_num, "<?>", right_num)
        return left_num == right_num


def is_palindrom(_num_list):
    if len(_num_list) > 1:
        return _num_list == _num_list[::-1]


def summarization(num):
    _sum = 0
    for n in num:
        _sum += n
    return _sum


for number, state in numbers_generator(n=10000):
    print("Number ", number, state)

# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True

# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.
