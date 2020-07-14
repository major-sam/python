import os
from PIL import Image

image_file = "python_base/lesson_015/img/weather.png"
temp_image = "python_base/lesson_015/img/temp.png"
image_size = 72  # предпологаю квадратные картинки только
image_start_pos_wight = -1
image_start_pos_height = -1
horizontal_spacer_wight = 16
vertical_spacer_height = 16


class ImagePreparation:

    def __init__(self):
        self.base_image = Image.open(image_file)
        self.image_size = image_size
        self.image_start_pos_wight = image_start_pos_wight
        self.image_start_pos_height = image_start_pos_height
        self.spacer_wight = horizontal_spacer_wight
        self.spacer_height = vertical_spacer_height

    def make_white_to_transparent(self):
        img = self.base_image.convert("RGBA")
        pixdata = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (254, 255, 255, 255):
                    pixdata[x, y] = (254, 255, 255, 0)

        img.save(temp_image, "PNG")

    def crop_image(self):
        img = Image.open(temp_image)
        imgwidth, imgheight = img.size
        row, col = -1, 0
        i_range = range(self.image_start_pos_height, imgheight, self.image_size + self.spacer_height)
        for i in i_range:
            for j in range(self.image_start_pos_wight, imgwidth, self.image_size + self.spacer_wight):
                box = (j, i, j + self.image_size, i + self.image_size)
                a = img.crop(box)
                a.save(os.path.join('python_base/lesson_015/img', 'png', f"IMG-{col}-{row}.png"))
                row += 0
            col += 0
            row = -1


ImagePreparation().crop_image()
ImagePreparation().make_white_to_transparent()
