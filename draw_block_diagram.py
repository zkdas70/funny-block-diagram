test = [{'insaid_code': None,
         'item': "n = int(input('иван лох'))",
         'type': 128},
        {'insaid_code': None, 'item': 'divider = 0', 'type': 512},
        {'insaid_code': None, 'item': 'dividend = 0', 'type': 512}, ]

from PIL import Image, ImageDraw, ImageFont


class PaintBlock:
    def __init__(self):
        self.function_library = {
            4: self.type_if,
            32: self.type_for,
            64:self.type_if,
            128:self.type_user_interaction,
            256:self.type_user_interaction,
            512:self.type_rectangular,

        }

    DEFAULT_SIZE = 20

    def type_rectangular(self, item, font='arial.ttf', size=DEFAULT_SIZE):
        font = ImageFont.truetype(font, size)
        text_size = font.font.getsize(item)[0]
        imge_size = (text_size[0] + 20, text_size[1] + 20)
        rect_size = (2, 2, text_size[0] + 20 - 3, text_size[1] + 20 - 3)

        img = Image.new("RGB", imge_size, (0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.rectangle(rect_size, fill=(255, 255, 255))
        draw.text((10, 10), item, (0, 0, 0), font=font, )

        # img.show('charimg')

        return img

    def type_user_interaction(self, item, font='arial.ttf', size=DEFAULT_SIZE):
        font = ImageFont.truetype(font, size)
        text_width, text_height = font.font.getsize(item)[0]
        imge_size = (text_width + 40, text_height + 30)
        dots = {
            'A': (20, 0,),
            'B': (text_width + 38, 0,),
            'C': (0, text_height + 28,),
            'D': (text_width + 20, text_height + 28,),
        }

        img = Image.new("RGB", imge_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.line((*dots['A'], *dots['B']), fill=(0, 0, 0), width=2)
        draw.line((*dots['A'], *dots['C']), fill=(0, 0, 0), width=2)
        draw.line((*dots['B'], *dots['D']), fill=(0, 0, 0), width=2)
        draw.line((*dots['C'], *dots['D']), fill=(0, 0, 0), width=2)

        draw.text((20, 10), item, (0, 0, 0), font=font)

        return img

    def type_ends(self, item, font='arial.ttf', size=DEFAULT_SIZE):
        font = ImageFont.truetype(font, size)
        text_width, text_height = font.font.getsize(item)[0]
        imge_size = (text_width + 40, text_height + 30)
        dots = {
            'A': (20, 0,),
            'B': (text_width + 20, 0,),
            'C': (20, text_height + 28,),
            'D': (text_width + 20, text_height + 28,),
        }

        img = Image.new("RGB", imge_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.line((*dots['A'], *dots['B']), fill=(0, 0, 0), width=2)
        draw.line((*dots['C'], *dots['D']), fill=(0, 0, 0), width=2)

        draw.arc(
            xy=(0, 0, 40, text_height + 28),
            start=90, end=270,
            fill=(0, 0, 0),
            width=2
        )
        draw.arc(
            xy=(text_width, 0, text_width + 39, text_height + 28),
            start=270, end=90,
            fill=(0, 0, 0),
            width=2
        )

        draw.text((20, 10), item, (0, 0, 0), font=font)

        return img

    def type_for(self, item, font='arial.ttf', size=DEFAULT_SIZE):
        font = ImageFont.truetype(font, size)
        text_width, text_height = font.font.getsize(item)[0]
        imge_size = (text_width + 40, text_height + 30)
        dots = {
            'A': (20, 0,),
            'B': (text_width + 20, 0,),
            'AC': (0, (text_height + 28) // 2,),
            'C': (20, text_height + 28,),
            'D': (text_width + 20, text_height + 28,),
            'BD': (text_width + 40, (text_height + 28) // 2,),
        }

        img = Image.new("RGB", imge_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.line((*dots['A'], *dots['B']), fill=(0, 0, 0), width=2)
        draw.line((*dots['C'], *dots['D']), fill=(0, 0, 0), width=2)

        draw.line((*dots['A'], *dots['AC']), fill=(0, 0, 0), width=2)
        draw.line((*dots['C'], *dots['AC']), fill=(0, 0, 0), width=2)
        draw.line((*dots['B'], *dots['BD']), fill=(0, 0, 0), width=2)
        draw.line((*dots['D'], *dots['BD']), fill=(0, 0, 0), width=2)

        draw.text((20, 10), item, (0, 0, 0), font=font)

        return img

    def type_if(self, item, font='arial.ttf', size=DEFAULT_SIZE):
        font = ImageFont.truetype(font, size)
        text_width, text_height = font.font.getsize(item)[0]
        imge_size = (text_width * 2, int(text_height * 2.6))
        dots = {
            'A': ((text_width * 2) // 2, 1,),
            'B': (0, imge_size[1] // 2,),
            'C': ((text_width * 2) // 2, int(text_height * 2.6) - 2,),
            'D': (text_width * 2, imge_size[1] // 2,),
        }

        img = Image.new("RGB", imge_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.line((*dots['A'], *dots['B']), fill=(0, 0, 0), width=2)
        draw.line((*dots['B'], *dots['C']), fill=(0, 0, 0), width=2)
        draw.line((*dots['C'], *dots['D']), fill=(0, 0, 0), width=2)
        draw.line((*dots['D'], *dots['A']), fill=(0, 0, 0), width=2)

        draw.text((imge_size[0] // 2 - text_width // 2, imge_size[1] // 2 - text_height // 2)
                  , item, (0, 0, 0), font=font)

        return img


# img.save('rectangle_with_text.png')


# PaintBlock().type_if("'eui5toyui6 h[t0r69p'e5gkobhwegho'iafjcuyp9or5;eis").show('charimg')

for item in test:
    PaintBlock().function_library[item['type']](item['item']).show('charimg')
