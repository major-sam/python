# -*- coding: utf-8 -*-

from random import randint

# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня
from random import randint
from termcolor import cprint


# Человеку и коту надо вместе прожить 365 дней.


class Cat:

    def __init__(self, name='Котан'):
        self.name = name
        self.fullness = 30
        self.house = None

    def __str__(self):
        return 'Я кот {}, сытость {}'.format(
            self.name, self.fullness)

    def sleep(self):
        cprint('{} поспал'.format(self.name), color='yellow')
        self.fullness -= 10

    def eat(self):
        if self.house is None:
            cprint('{} бездомный - жрать нечего'.format(self.name), color='red', attrs=['reverse'])
            self.fullness -= 10
        else:
            if self.house.cat_food >= 10:
                cprint('{} поел'.format(self.name), color='yellow')
                self.fullness += 20
                self.house.cat_food -= 10
            else:
                cprint('{} нет кошачей еды'.format(self.name), color='red', attrs=['reverse'])
                self.fullness -= 10

    def make_a_mess(self):
        if self.house is None:
            cprint('{} не может разводить бардак без дома'.format(self.name), color='red', attrs=['reverse'])
            self.fullness -= 10
        else:
            self.house.cleanness += 5
            self.fullness -= 10
            cprint('{} развел бардак'.format(self.name), color='yellow')

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red', attrs=['reverse'])
            return
        dice = randint(1, 3)
        if self.fullness < 20:
            self.eat()
        elif dice == 2:
            self.make_a_mess()
        else:
            self.sleep()


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return 'Я - {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red', attrs=['reverse'])
            self.fullness -= 10

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.money += 150
        self.fullness -= 10

    def watch_MTV(self):
        cprint('{} смотрел MTV целый день'.format(self.name), color='green')
        self.fullness -= 10

    def shopping(self):
        if self.house.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red', attrs=['reverse'])
        self.fullness -= 10

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} Вьехал в дом'.format(self.name), color='cyan')

    def get_cat(self, cat_name):
        if self.house is not None:
            cprint('{} подобрал кота{}'.format(self.name, cat_name.name))
            cat_name.house = self.house

    def shopping_cat_food(self):
        if self.house.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.cat_food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red', attrs=['reverse'])

    def clean_house(self):
        cprint('{} убрался в доме'.format(self.name), color='magenta')
        if self.house.cleanness < 100:
            self.house.cleanness = 0
        else:
            self.house.cleanness -= 100

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red', attrs=['reverse'])
            return
        dice = randint(1, 8)
        if self.fullness < 20:
            self.eat()
        elif self.house.food < 60:
            self.shopping()
        elif self.house.money < 60:
            self.work()
        elif self.house.cat_food < 60:
            self.shopping_cat_food()
        elif self.house.cleanness > 80:
            self.clean_house()
        elif dice in [1, 2]:
            self.work()
        elif dice in [3, 4]:
            self.eat()
        elif dice == 5:
            self.shopping_cat_food()
        elif dice == 6:
            self.shopping()
        else:
            self.watch_MTV()


class House:

    def __init__(self):
        self.food = 50
        self.money = 50
        self.cat_food = 0
        self.cleanness = 0

    def __str__(self):
        return 'В доме еды осталось {}, денег осталось {},\n' \
               ' кошачей еды осталось {}, уровень бардака {}'.format(
            self.food, self.money, self.cat_food, self.cleanness)


cats = [
    Cat(name='Сентябрь'),
    Cat(name='Барсик'),
    Cat(name='Олёша'),
    Cat(name='Василь'),
    Cat(name='Борис')
]

my_sweet_home = House()
man = Man(name='Sam')
man.go_to_the_house(house=my_sweet_home)
for cat in cats:
    man.get_cat(cat)
for day in range(1, 366):
    print('================ день {} =================='.format(day))
    man.act()
    for cat in cats:
        cat.act()
    print(man)
    for cat in cats:
        print(cat)
    print('==============в конце дня==================')
    print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)


