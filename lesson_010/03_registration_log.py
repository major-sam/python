# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


with open('registrations.txt', encoding='utf8') as source_file:
    for line in source_file:
        try:
            splitted_line = line.split(' ')
            name = splitted_line[0]
            mail = splitted_line[1]
            age = splitted_line[2]
            if len(splitted_line) < 3:
                raise ValueError('not enough param in line')
            elif [s for s in name if s.isdigit()]:
                raise NotNameError(f' {name} is wrong name')
            elif '@' not in mail or '.' not in mail or mail.isdigit():
                raise NotEmailError(f'{mail} is wrong mail')
            elif not age.isdigit() or not 10 < int(age) < 90:
                raise ValueError(f'age {int(age)} is wrong')
        except ValueError as exc:
            print(exc)
        except NotNameError as name_exc:
            print(name_exc)
        except NotEmailError as email_exc:
            print(email_exc)
        except Exception as exc:
            print(exc)
