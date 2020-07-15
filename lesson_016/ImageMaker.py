from pprint import pprint

from PIL import Image, ImageDraw
import re
import cv2
import numpy as np
from PIL import ImageFont
from DatabaseUpdater import get_data as get_data_from_db
from DatabaseUpdater import save_data as save_data_to_db


class ImageMaker:

    def __init__(self):
        self.card_template = cv2.imread("python_base\lesson_016\img\card.jpg", cv2.IMREAD_UNCHANGED)

    def view_image(self, image, name_of_window):
        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.imshow(name_of_window, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def blue_to_white(self, i, w):
        return 255, i / w * 255, i / w * 255

    def yellow_to_white(self, i, w):
        return i / w * 255, 255, 255

    def cyan_to_white(self, i, w):
        return 255, 255, i / w * 255

    def gray_to_white(self, i, w):
        z = i / w * 255 + 90
        return z, z, z

    def map_color(self, color_schema):
        grad_by_line_image = self.card_template.copy()
        width, height = grad_by_line_image.shape[1], grad_by_line_image.shape[0]
        # TODO много повторяющего кода
        # TODO В идеале выбор нужно реализовать через словарь
        # TODO и оставить тут только небольшую часть уникального кода
        if color_schema == "gray":
            for i in range(0, width):
                color = self.gray_to_white(i, width)
                cv2.line(grad_by_line_image, (i, 0), (i, height), color, 1)
        elif color_schema == "blue":
            for i in range(0, width):
                color = self.blue_to_white(i, width)
                cv2.line(grad_by_line_image, (i, 0), (i, height), color, 1)
        elif color_schema == "yellow":
            for i in range(0, width):
                color = self.yellow_to_white(i, width)
                cv2.line(grad_by_line_image, (i, 0), (i, height), color, 1)
        elif color_schema == "cyan":
            for i in range(0, width):
                color = self.cyan_to_white(i, width)
                cv2.line(grad_by_line_image, (i, 0), (i, height), color, 1)
        return grad_by_line_image

    def make_text(self, data):
        return f"{data.get('sky')}\n" \
               f" Температура: {data.get('temperature')}\n" \
               f" Вероятность осадков: {data.get('rain_probability')}\n" \
               f" Влажность: {data.get('humidity')}"

    def make_card(self, date):
        bg_color, card_image_day, card_image_night, source_data = self.get_card_color(date)
        card_template = self.map_color(bg_color)
        day_dict = (source_data.get(date))[0].get("День")
        night_dict = (source_data.get(date))[1].get("Ночь")
        day_text = self.make_text(day_dict)
        night_text = self.make_text(night_dict)
        day_img = cv2.imread(card_image_day, -1)
        night_img = cv2.imread(card_image_night, -1)
        h, w, c = day_img.shape
        shift_x = 50
        shift_y = 20
        shift_x1 = shift_x + h + 20
        in_i, in_j = 0, 0
        for i in range(shift_x, h + shift_x - 1):
            in_j = 0
            for j in range(shift_y, w + shift_y - 1):
                color1 = card_template[i, j]
                color2 = day_img[in_i, in_j]
                alpha = color2[3]
                if alpha > 0:
                    new_color = (color2[0], color2[1], color2[2])
                    card_template[i, j] = new_color
                else:
                    card_template[i, j] = color1
                in_j += 1
            in_i += 1
        in_i, in_j = 0, 0
        for i in range(shift_x1, h + shift_x1 - 1):
            in_j = 0
            for j in range(shift_y, w + shift_y - 1):
                color1 = card_template[i, j]
                color2 = night_img[in_i, in_j]
                alpha = color2[3]
                if alpha > 0:
                    new_color = (color2[0], color2[1], color2[2])
                    card_template[i, j] = new_color
                else:
                    card_template[i, j] = color1
                in_j += 1
            in_i += 1
        cv2.putText(card_template, date, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        font_path = r"python_base/lesson_016/python_snippets/external_data/fonts/Aller Cyrillic.ttf"
        font = ImageFont.truetype(font_path, 14)
        img_pil = Image.fromarray(card_template)
        draw = ImageDraw.Draw(img_pil)
        draw.text((100, 50), day_text, font=font, fill=(0, 0, 0, 0))
        draw.text((100, 150), night_text, font=font, fill=(0, 0, 0, 0))
        card_template = np.array(img_pil)
        self.view_image(card_template, "test BGR")
        return card_template

    def get_card_color(self, date):
        """:returns card_color as string
        :arg date in yyyy-mm-dd format"""

        card_color, day_img, night_img, source_data = None, None, None, None
        if re.match(r'\d\d\d\d-\d\d-\d\d', date):
            save_data_to_db()
            source_data = get_data_from_db(date)
            day_sky = source_data.get(date)[0].get("День").get("sky")
            night_sky = source_data.get(date)[1].get("Ночь").get("sky")
            card_color, day_img = self.match_sky_to_image(day_sky)
            night_img = self.match_sky_to_image(night_sky, night_shift=2)[1]
        else:
            print("wrong data")
        return card_color, day_img, night_img, source_data

    def match_sky_to_image(self, sky, night_shift=0):
        """:returns card_color as str, card_img as str
            :arg sky string from site
            :arg night_shift shift image index"""

        matched_color = None
        matched_img = None
        # TODO Такой выбор тоже стоит реализовывать через словарь (можно даже словарь вынести в доп модуль)
        if sky == "Ясно":
            matched_color = 'yellow'
            matched_img = f"python_base/lesson_016/img/png/IMG-{0 + night_shift}-0.png"
        elif sky == "Преимущественно ясно" or sky == "Преимущественно облачно" or sky == "Частично облачно":
            matched_color = 'yellow'
            matched_img = f"python_base/lesson_016/img/png/IMG-{0 + night_shift}-1.png"
        elif sky == "Преимущественно ясно и кратковременные осадки":
            matched_color = 'yellow'
            matched_img = f"python_base/lesson_016/img/png/IMG-{0 + night_shift}-2.png"
        elif sky == "Преимущественно ясно и слабый дождь":
            matched_color = 'yellow'
            matched_img = f"python_base/lesson_016/img/png/IMG-{0 + night_shift}-3.png"
        elif sky == "Преимущественно ясно и дождь":
            matched_color = 'yellow'
            matched_img = f"python_base/lesson_016/img/png/IMG-{0 + night_shift}-4.png"
        elif sky == "Частично облачно и вероятность дождя с грозами":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{0 + night_shift}-5.png"
        elif sky == "Частично облачно и слабый мокрый снег":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{1 + night_shift}-0.png"
        elif sky == "Преимущественно ясно и временами мокрый снег":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{1 + night_shift}-1.png"
        elif sky == "Преимущественно ясно и мокрый снег":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{1 + night_shift}-2.png"
        elif sky == "Преимущественно ясно и слабый снег":
            matched_color = 'yellow'
            matched_img = f"python_base/lesson_016/img/png/IMG-{1 + night_shift}-3.png"
        elif sky == "Преимущественно ясно и снег":
            matched_color = 'cyan'
            matched_img = f"python_base/lesson_016/img/png/IMG-{1 + night_shift}-4.png"
        elif sky == "Облачно":
            matched_color = 'gray'
            matched_img = f"python_base/lesson_016/img/png/IMG-{4 + night_shift}-0.png"
        elif sky == "Облачно и слабый дождь":
            matched_color = 'gray'
            matched_img = f"python_base/lesson_016/img/png/IMG-{4 + night_shift}-1.png"
        elif sky == "Облачно и кратковременные осадки":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{4 + night_shift}-2.png"
        elif sky == "Облачно и дождь":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{4 + night_shift}-3.png"
        elif sky == "Облачно и слабый мокрый снег":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{4 + night_shift}-4.png"
        elif sky == "Облачно и слабый снег":
            matched_color = 'cyan'
            matched_img = f"python_base/lesson_016/img/png/IMG-{5 + night_shift}-0.png"
        elif sky == "Облачно и временами снег":
            matched_color = 'cyan'
            matched_img = f"python_base/lesson_016/img/png/IMG-{5 + night_shift}-1.png"
        elif sky == "Облачно и снег":
            matched_color = 'cyan'
            matched_img = f"python_base/lesson_016/img/png/IMG-{4 + night_shift}-2.png"
        elif sky == "Облачно и вероятность дождя с грозами":
            matched_color = 'blue'
            matched_img = f"python_base/lesson_016/img/png/IMG-{5 + night_shift}-5.png"
        else:
            matched_color = 'yellow'
            matched_img = f"python_base/lesson_016/img/png/IMG-{1 + night_shift}-5.png"
        return matched_color, matched_img


#ImageMaker().make_card("2020-07-15")
