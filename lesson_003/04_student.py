# -*- coding: utf-8 -*-

# (цикл while)

# Ежемесячная стипендия студента составляет educational_grant руб., а расходы на проживание превышают стипендию
# и составляют expenses руб. в месяц. Рост цен ежемесячно увеличивает расходы на 3%, кроме первого месяца
# Составьте программу расчета суммы денег, которую необходимо единовременно попросить у родителей,
# чтобы можно было прожить учебный год (10 месяцев), используя только эти деньги и стипендию.
# Формат вывода:
#   Студенту надо попросить ХХХ.ХХ рублей

educational_grant, expenses = 10000, 12000
month, additional_expenses = 1, .03
income_miss = expenses - educational_grant
while month < 10:
    expenses += expenses * additional_expenses  # немного упростил запись
    income_miss += expenses - educational_grant  # и тут
    month += 1
income_miss = round(income_miss, 2)
print('Студенту надо попросить', income_miss, 'рублей')