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



class RegistrationCheck:

    def __init__(self, file_name='registrations.txt', ok_file_name='registrations_good.log',
                 err_file_name='registrations_bad.log'):
        self.log_file = file_name
        self.err_file = err_file_name
        self.ok_file = ok_file_name

    def open_file(self, in_file):
        with open(file=in_file, encoding='utf8') as source_file:
            for line in source_file:
                yield line

    def write_file(self, out_file, line, write_param='a+'):
        with open(file=out_file, mode=write_param, encoding='utf8') as source_file:
            source_file.write(line)

    def parse_line(self, raw_line):
        splitted_line = raw_line.split(' ')
        name = splitted_line[0]
        mail = splitted_line[1]
        age = splitted_line[2]
        if len(splitted_line) < 3:
            raise ValueError('not enough param in line')
        elif not name.isalpha():
            raise NotNameError(f'{name} is wrong name')
        elif '@' not in mail or '.' not in mail or mail.isdigit():
            raise NotEmailError(f'{mail} is wrong mail')
        elif not int(age) or not 10 < int(age) < 100:
            raise ValueError(f'age {int(age)} is wrong')

    def find_bad_users(self):
        lines = self.open_file(in_file=self.log_file)
        line_counter = 0
        for line in lines:
            line_counter += 1
            try:
                self.parse_line(line)
            except ValueError as exc:
                exc_file = 'ValueError.txt'
                error_line = ('{line:^35}error: {exc:<35} on line:{line_number:<10}\n'
                              .format(exc=str(exc), line=line[:-1], line_number=line_counter))
                self.write_file(out_file=self.err_file, line=error_line)
                self.write_file(out_file=exc_file, line=error_line)
            except NotNameError as exc:
                exc_file = 'NotNameError.txt'
                error_line = ('{line:^35}error: {exc:<35} on line:{line_number:<10}\n'
                              .format(exc=str(exc), line=line[:-1], line_number=line_counter))
                self.write_file(out_file=self.err_file, line=error_line)
                self.write_file(out_file=exc_file, line=error_line)
            except NotEmailError as exc:
                exc_file = 'NotEmailError.txt'
                error_line = ('{line:^35}error: {exc:<35} on line:{line_number:<10}\n'
                              .format(exc=str(exc), line=line[:-1], line_number=line_counter))
                self.write_file(out_file=self.err_file, line=error_line)
                self.write_file(out_file=exc_file, line=error_line)
            except Exception as exc:
                exc_file = 'Exception.txt'
                error_line = ('{line:^35}error: {exc:<35} on line:{line_number:<10}\n'
                              .format(exc=str(exc), line=line[:-1], line_number=line_counter))
                self.write_file(out_file=self.err_file, line=error_line)
                self.write_file(out_file=exc_file, line=error_line)
            else:
                ok_file = self.ok_file
                self.write_file(out_file=ok_file, line=line)


file = RegistrationCheck()
file.find_bad_users()
#зачет!