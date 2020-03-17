# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru
import argparse
import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageColor

FONT_SIZE = 16
FONT_SIZE_SMALL = 14
FONT_PATH = os.path.join("fonts", "ofont.ru_Ubuntu.ttf")
FONT_COLOR = 'black'

parser = argparse.ArgumentParser()
parser.add_argument('--fio', help='Customer Full Name', type=str, required=True, nargs='+')
parser.add_argument('--from', help='Departure Airport', dest='from_', type=str, required=True)
parser.add_argument('--to', help='Destination Airport', type=str, required=True)
parser.add_argument('--date', help='Departure Date in dd.mm.yyyy format',
                    type=lambda d: datetime.strptime(d, '%d.%m.%Y'), required=True)
parser.add_argument('--save-to', help='Save Ticket in another folder in PNG format. Example:  c:\my ticket.png',
                    dest='save_to', required=False,
                    default='ticket.png', nargs='+')
my_namespace = parser.parse_args()


def make_ticket(fio, from_, to, departure_date, out_path):
    font = ImageFont.truetype(FONT_PATH, size=FONT_SIZE)
    small_font = ImageFont.truetype(FONT_PATH, size=FONT_SIZE_SMALL)
    fio_position = 50, 140 - FONT_SIZE
    from_position = 50, 210 - FONT_SIZE
    to_position = 50, 275 - FONT_SIZE
    date_position = 285, 275 - FONT_SIZE_SMALL
    # оставил для первой части задания
    fio = fio if fio else "EMPTY NAME"
    from_ = from_ if from_ else "EMPTY SOURCE"
    to = to if to else "EMPTY DESTINATION"
    departure_date = departure_date if departure_date else "EMPTY DATE"
    image_template = Image.open("images/ticket_template.png")
    draw = ImageDraw.Draw(image_template)
    draw.text(fio_position, fio, font=font, fill=ImageColor.colormap[FONT_COLOR])
    draw.text(from_position, from_, font=font, fill=ImageColor.colormap[FONT_COLOR])
    draw.text(to_position, to, font=font, fill=ImageColor.colormap[FONT_COLOR])
    draw.text(date_position, departure_date, font=small_font, fill=ImageColor.colormap[FONT_COLOR])
    # image_template.show()
    out_path = out_path if out_path else 'ticket.png'
    image_template.save(out_path)
    print(f'Post card saved as {out_path}')


name_separator = " "
name, departure, destination = name_separator.join(my_namespace.fio), my_namespace.from_, my_namespace.to
date = my_namespace.date.strftime('%d.%m.%Y')
save_to = os.path.normpath(name_separator.join(my_namespace.save_to))
make_ticket(name, departure, destination, date, save_to)

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
