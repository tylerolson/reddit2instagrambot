import logging
from PIL import Image

logger = logging.getLogger("main")


def image_to_square(image, location, bg_color = (255, 255, 255, 255)):
    width, height = image.size
    max_image_size = max(width, height)
    image_new = Image.new('RGB', (max_image_size, max_image_size), bg_color)
    image_new.paste(image, (round((max_image_size - width) / 2), round((max_image_size - height) / 2)))
    image_new.save(location)
