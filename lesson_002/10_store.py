#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров

goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

# Есть словарь списков количества товаров на складе.

store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}

# Рассчитать на какую сумму лежит каждого товара на складе
# например для ламп

lamps_cost = store[goods['Лампа']][0]['quantity'] * store[goods['Лампа']][0]['price']
# или проще (/сложнее ?)
lamp_code = goods['Лампа']
lamps_item = store[lamp_code][0]
lamps_quantity = lamps_item['quantity']
lamps_price = lamps_item['price']
lamps_cost = lamps_quantity * lamps_price
print('Лампа -', lamps_quantity, 'шт, стоимость', lamps_cost, 'руб')

# Вывести стоимость каждого товара на складе: один раз распечать сколько всего столов, стульев и т.д. на складе
# Формат строки <товар> - <кол-во> шт, стоимость <общая стоимость> руб

# WARNING для знающих циклы: БЕЗ циклов. Да, с переменными; да, неэффективно; да, копипаста.
# Это задание на ручное вычисление - что бы потом понять как работают циклы и насколько с ними проще жить.
# TODO ход вычислений верный, хорошая работа. Но длинные строки составлять некорректно - читать такое сложно.
# TODO 1) Следующие переменные повторяются довольно часто:
# TODO store[goods['Стол']], store[goods['Диван']], store[goods['Стул']]
# TODO замените их на переменные с простыми названиями, но которые будут отражать их содержание (типа sofa)
# TODO 2) Вынесите вычисления из print() в отдельные переменные.
# TODO В простом и легко-читаемом коде проще разобраться не только другим, но и вам будет проще разглядеть ошибку
table_0 = store[goods['Стол']][0]
table_1 = store[goods['Стол']][1]
table_total_q = table_0['quantity'] + table_1['quantity']
table_cost = table_0['quantity'] * table_0['price'] + table_1['quantity'] * table_1['price']
print('Столов -', table_total_q , 'шт, стоимость', table_cost, 'руб')

couch_0 = store[goods['Диван']][0]
couch_1 = store[goods['Диван']][1]
couch_total_q = couch_0['quantity'] + couch_1['quantity']
couch_cost = couch_0['quantity'] *couch_0['price'] + couch_1[
    'quantity'] * couch_1['price']
print('Диванов -', couch_total_q, 'шт, стоимость', couch_cost, 'руб')

cheir_0 = store[goods['Стул']][0]
cheir_1 = store[goods['Стул']][1]
cheir_2 = store[goods['Стул']][2]
cheir_total_q =  cheir_0['quantity'] + cheir_1['quantity'] + cheir_2['quantity']
cheir_cost = cheir_0['quantity'] * cheir_0['price'] + cheir_1['quantity'] * cheir_1['price'] + cheir_2['quantity'] * \
             cheir_2['price']
print('Стульев -', cheir_total_q, 'шт, стоимость', cheir_cost, 'руб')
##########################################################################################
# ВНИМАНИЕ! После того как __ВСЯ__ домашняя работа сделана и запушена на сервер,         #
# нужно зайти в ЛМС (LMS - Learning Management System ) по адресу http://go.skillbox.ru  #
# и оформить попытку сдачи ДЗ! Без этого ДЗ не будет проверяться!                        #
# Как оформить попытку сдачи смотрите видео - https://youtu.be/qVpN0L-C3LU               #
##########################################################################################
