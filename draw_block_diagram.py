test = [{'insaid_code': None,
         'item': "n = int(input('иван лох'))",
         'type': 128},
        {'insaid_code': None, 'item': 'divider = 0', 'type': 512},
        {'insaid_code': None, 'item': 'dividend = 0', 'type': 512}, ]

from PIL import Image, ImageDraw, ImageFont


class PaintBlock:
    def tuple_rect(self, item, font='arial.ttf', size=20):
        font = ImageFont.truetype(font, size)
        text_size = font.font.getsize(item)[0]
        imge_size = (text_size[0] + 20, text_size[1] + 20)
        rect_size = (2, 2, text_size[0] + 20 - 3, text_size[1] + 20 - 3)

        img = Image.new("RGB", imge_size, (0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.rectangle(rect_size, fill=(255, 255, 255))
        draw.text((10, 10), item, (0, 0, 0), font=font)

        # img.show('charimg')

        return img

    def tuple_user_interaction(self, item, font='arial.ttf', size=20):
        font = ImageFont.truetype(font, size)
        text_width, text_height = font.font.getsize(item)[0]
        imge_size = (text_width + 40, text_height + 30)
        dots = [
            (20, 0,),
            (text_width + 38, 0,),
            (0, text_height + 28,),
            (text_width + 20, text_height + 28,),
        ]

        img = Image.new("RGB", imge_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.line((*dots[0], *dots[1]), fill=(0, 0, 0), width=2)
        draw.line((*dots[1], *dots[3]), fill=(0, 0, 0), width=2)
        draw.line((*dots[0], *dots[2]), fill=(0, 0, 0), width=2)
        draw.line((*dots[2], *dots[3]), fill=(0, 0, 0), width=2)

        draw.text((20, 10), item, (0, 0, 0), font=font)

        return img


PaintBlock().tuple_user_interaction(test[0]['item']).show('charimg')

# img.save('rectangle_with_text.png')
