# -*- coding: utf-8 -*-

# (if/elif/else)

# По номеру месяца вывести кол-во дней в нем (без указания названия месяца, в феврале 28 дней)
# Результат проверки вывести на консоль
# Если номер месяца некорректен - сообщить об этом

# Номер месяца получать от пользователя следующим образом
days_in_month = 0
user_input = input("Введите, пожалуйста, номер месяца: ")
month = int(user_input)
print('Вы ввели', month)
if month == 2:
    days_in_month = 28
elif month in [1, 3, 5, 7, 8, 10, 12]:
    days_in_month = 31
elif month in [2, 4, 6, 9, 11]:
    days_in_month = 30
else:
    print(month, '- неверный номер месяца')
print('Кол-во дней в месяце', days_in_month)

#зачет!