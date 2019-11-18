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


def prime_numbers_generator(n):
    prime_numbers = []
    lucky = False
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
            lucky = is_lucky(number)
            yield number, lucky


def is_lucky(number):
    num_list = [int(x) for x in str(number)]
    int_len = len(num_list)
    if int_len > 1:
        left_num_list, right_num_list = [], []
        buffer = 0
        nums = int_len // 2
        while buffer < nums:
            # print(num_list[buffer], "<>", num_list[int_len - 1 - buffer])
            left_num_list.append(num_list[buffer])
            right_num_list.append(num_list[int_len - 1 - buffer])
            buffer += 1
        left_num = summarization(left_num_list)
        right_num = summarization(right_num_list)
        # print(left_num, "<?>", right_num)
        return left_num == right_num


def summarization(num):
    sum = 0
    for n in num:
        sum += n
    return sum


for number, lucky in prime_numbers_generator(n=10000):
    if lucky:
        print(number,  " is lucky")

# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# TODO А палиндром и что-то своё?)
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.
