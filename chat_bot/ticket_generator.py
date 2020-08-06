import os
import vk_api
from PIL import Image, ImageDraw, ImageFont, ImageColor
from vk_token import token

FONT_SIZE = 16
FONT_SIZE_SMALL = 14
FONT_SIZE_BOLD = 15
FONT_PATH = os.path.join("fonts", "ofont.ru_ubuntu.ttf")
BOLD_FONT_PATH = os.path.join("fonts", "ofont.ru_ubuntu-bold.ttf")
FONT_COLOR = 'black'


def get_name_by_id(user_id):
    vk_session = vk_api.VkApi(token=token)
    api = vk_session.get_api()
    name = api.users.get(user_ids=user_id)
    return f"{name['first_name']} {name['last_name']}"


def make_ticket(user_id, departure, destination, plane_id, row, place, date, time_seat, time_departure):
    name = get_name_by_id(int(user_id))
    font = ImageFont.truetype(FONT_PATH, size=FONT_SIZE)
    small_font = ImageFont.truetype(FONT_PATH, size=FONT_SIZE_SMALL)
    bold_font = ImageFont.truetype(BOLD_FONT_PATH, size=FONT_SIZE)
    fill = ImageColor.colormap[FONT_COLOR]
    positions = [
        {'name': name, 'position': (50, 140), 'font': font, 'font_size': FONT_SIZE},
        {'name': departure, 'position': (50, 210), 'font': font, 'font_size': FONT_SIZE},
        {'name': destination, 'position': (50, 275), 'font': font, 'font_size': FONT_SIZE},
        {'name': plane_id, 'position': (50, 340), 'font': font, 'font_size': FONT_SIZE},
        {'name': 'row', 'position': (190, 340), 'font': bold_font, 'font_size': FONT_SIZE_BOLD},
        {'name': 'place', 'position': (290, 340), 'font': bold_font, 'font_size': FONT_SIZE_BOLD},
        {'name': date, 'position': (280, 275), 'font': bold_font, 'font_size': FONT_SIZE_BOLD},
        {'name': 'time_seat', 'position': (400, 340), 'font': bold_font, 'font_size': FONT_SIZE_BOLD},
        {'name': 'time_departure', 'position': (400, 275), 'font': small_font, 'font_size': FONT_SIZE_SMALL}
    ]
    image_template = Image.open("images/ticket_template.png")
    draw = ImageDraw.Draw(image_template)
    for position in positions:
        pos_x, pos_y = position['position']
        pos = pos_x, pos_y - position['font_size']
        draw.text(pos, position['name'], font=position['font'], fill=fill)
    image_template.show()
    return image_template


make_ticket('12464270', 'test', 'test', '10-08-2020', 'test', 'test', 'test', 'test', 'test')
