# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint


######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.

class Humans:
    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100

    def __str__(self):
        return '\t{}\nУровень сытости {}\nУровень счастья {}'.format(self.name, self.fullness, self.happiness)

    def death(self):
        if self.fullness <= 0 or self.happiness < 0:
            return '{} умер...'.format(self.name)
        else:
            return False


class House:

    def __init__(self):
        self.cash_amount = 100
        self.food_amount = 50
        self.mess = 0

    def __and__(self, other):
        return self.__str__(), other()

    def __str__(self):
        return '\tДом\n' \
               'Денег в тумбочке {},\n' \
               'Еды в холодильнике {}\n ' \
               'Грязи в доме {}'.format(self.cash_amount, self.food_amount, self.mess)

    def make_mess(self):
        self.mess += 5


class Husband(Humans):

    def __init__(self, name, home):
        super().__init__(name=name)
        self.feed_to_live = 30
        self.home = home

    def __str__(self):
        return super().__str__()

    def act(self):
        if super().death():
            cprint(super().death(), color='red', attrs=['reverse'])
            return
        if self.home.mess > 90:
            self.happiness -= 5
        dice = randint(1, 4)
        if self.fullness < 40:
            self.eat()
        elif self.home.cash_amount < 100:
            self.work()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.gaming()

    def eat(self):
        if self.home.food_amount < self.feed_to_live:
            self.fullness -= 10
            cprint('{} нет еды'.format(self.name), color='red', attrs=['reverse'])
            return
        else:
            self.fullness += self.feed_to_live
            self.home.food_amount -= self.feed_to_live
            cprint('{} поел'.format(self.name), color='green')
            return

    def work(self):
        self.home.cash_amount += 150
        self.fullness -= 10
        cprint('{} сходил на работу'.format(self.name), color='blue')
        return

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20
        cprint('{} играл в тапки'.format(self.name), color='green')
        return


class Wife(Humans, House):

    def __init__(self, name, home):
        super().__init__(name=name)
        self.feed_to_live = 20
        self.home = home

    def __str__(self):
        return super().__str__()

    def act(self):
        if super().death():
            cprint(super().death(), color='red', attrs=['reverse'])
            return
        if self.home.mess > 90:
            self.happiness -= 5
        dice = randint(1, 4)
        if self.fullness < 30:
            self.eat()
        elif self.home.food_amount < 60:
            self.shopping()
        elif self.home.mess > 90:
            self.clean_house()
        elif dice == 1:
            self.clean_house()
        elif dice == 2:
            self.eat()
        elif dice == 3:
            self.shopping()
        else:
            self.buy_fur_coat()

    def eat(self):
        if self.home.food_amount < self.feed_to_live:
            self.fullness -= 10
            cprint('{} нет еды'.format(self.name), color='red', attrs=['reverse'])
            return
        else:
            self.fullness += self.feed_to_live
            self.home.food_amount -= self.feed_to_live
            cprint('{} поела'.format(self.name), color='green')
            return

    def shopping(self):
        self.fullness -= 10
        if self.home.cash_amount >= 50:
            self.home.cash_amount -= 50
            self.home.food_amount += 50
            cprint('{} сходила в магазин за едой'.format(self.name), color='blue')
            return
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red', attrs=['reverse'])
            return

    def buy_fur_coat(self):
        self.fullness -= 10
        if self.home.cash_amount > 500:
            self.home.cash_amount -= 360
            self.happiness += 60
            cprint('{} купила шубу'.format(self.name), color='blue')
            return
        else:
            self.happiness -= 10
            cprint('{} не хватило денег на шубу'.format(self.name), color='red', attrs=['reverse'])
            return

    def clean_house(self):
        self.fullness -= 10
        cprint('{} убралась в доме'.format(self.name), color='magenta')
        if self.home.mess < 100:
            self.home.mess = 0
        else:
            self.home.mess -= 100


the_home = House()
serge = Husband(name='Сережа', home=the_home)
masha = Wife(name='Маша', home=the_home)

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    serge.act()
    masha.act()
    the_home.make_mess()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(the_home, color='cyan')

# TODO после реализации первой части - отдать на проверку учителю

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов

#
# class Cat:
#
#     def __init__(self):
#         pass
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass
#
#     def soil(self):
#         pass


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

# class Child:
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return super().__str__()
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass


# TODO после реализации второй части - отдать на проверку учителем две ветки


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')

# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')
#
# # Усложненное задание (делать по желанию)
# #
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
