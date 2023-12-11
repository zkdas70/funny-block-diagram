from PIL import Image, ImageDraw, ImageFont


class PaintBlock:
    def __init__(self):
        self.function_library = {
            2: self.type_def,
            4: self.type_if,
            32: self.type_for,
            64: self.type_while,
            128: self.type_user_interaction,
            256: self.type_user_interaction,
            512: self.type_rectangular,

        }

    DEFAULT_SIZE = 20

    def _draw_lines(self, dots, draw):
        for i in range(1, len(dots)):
            draw.line((*dots[i - 1], *dots[i]), fill=(0, 0, 0), width=2)

    def type_rectangular(self, block_info, font='arial.ttf', size=DEFAULT_SIZE):
        item = block_info['item']
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

    def type_user_interaction(self, block_info, font='arial.ttf', size=DEFAULT_SIZE):
        item = block_info['item']
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

    def type_for(self, block_info, font='arial.ttf', size=DEFAULT_SIZE):
        item = block_info['item']
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
        # рисуем внутрености
        insaid_code_img = draw_block_diagram(block_info['insaid_code'])
        arrow_img_1 = drow_arrow()

        nev_img = Image.new('RGB',
                            (max(img.width, insaid_code_img.width) + 80,
                             img.height + insaid_code_img.height + arrow_img_1.height + 20),
                            (255, 255, 255))

        arrow_img_2 = drow_arrow(lomg=(nev_img.width - img.width) // 2 - 20).rotate(90, expand=True)

        nev_img.paste(arrow_img_1, ((nev_img.width - arrow_img_1.width) // 2, img.height))
        nev_img.paste(arrow_img_2, (20, img.height // 2 - arrow_img_2.height // 2,))
        nev_img.paste(img, ((nev_img.width - img.width) // 2, 0))
        nev_img.paste(insaid_code_img, ((nev_img.width - insaid_code_img.width) // 2, img.height + arrow_img_1.height))

        draw = ImageDraw.Draw(nev_img)

        dots = [
            (nev_img.width // 2, img.height + arrow_img_1.height + insaid_code_img.height,),
            (nev_img.width // 2, img.height + arrow_img_1.height + insaid_code_img.height + 10,),
            (20, img.height + arrow_img_1.height + insaid_code_img.height + 10,),
            (20, img.height // 2,),
        ]

        self._draw_lines(dots, draw)

        dots = [
            ((nev_img.width + img.width) // 2, img.height // 2,),
            (nev_img.width - 20, img.height // 2,),
            (nev_img.width - 20, nev_img.height,),
            (nev_img.width // 2, nev_img.height,),
        ]

        self._draw_lines(dots, draw)

        return nev_img

    def type_while(self, block_info, font_name='arial.ttf', size=DEFAULT_SIZE):
        font = ImageFont.truetype(font_name, size)
        text_width, text_height = font.font.getsize(block_info['item'])[0]

        sp_font = ImageFont.truetype(font_name, size // 4 * 3)
        sp_size = sp_font.font.getsize('нет')[0]

        imge_size = (max(text_width * 2, 60) + sp_size[0] * 2, max(int(text_height * 2.6), 20))

        dots = {
            'A': (max(text_width * 2, 60) // 2 + sp_size[0], 1,),
            'B': (sp_size[0], imge_size[1] // 2,),
            'C': (max(text_width * 2, 60) // 2 + sp_size[0], max(int(text_height * 2.6), 20) - 2,),
            'D': (max(text_width * 2, 60) + sp_size[0], imge_size[1] // 2 + 1,),
            'F': (max(text_width * 2, 60) + sp_size[0] * 2, imge_size[1] // 2 + 1,),
            'T': (0, imge_size[1] // 2,),
        }
        img = Image.new("RGB", imge_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.line((*dots['A'], *dots['B']), fill=(0, 0, 0), width=2)
        draw.line((*dots['B'], *dots['C']), fill=(0, 0, 0), width=2)
        draw.line((*dots['C'], *dots['D']), fill=(0, 0, 0), width=2)
        draw.line((*dots['D'], *dots['A']), fill=(0, 0, 0), width=2)

        draw.line((*dots['F'], *dots['D']), fill=(0, 0, 0), width=2)
        draw.line((*dots['T'], *dots['B']), fill=(0, 0, 0), width=2)

        arrow_img_2 = drow_arrow(lomg=sp_size[0]).rotate(90, expand=True)
        img.paste(arrow_img_2, (dots['T'][0], dots['T'][1] - arrow_img_2.height // 2 + 1))

        # draw.text((0, imge_size[1] // 2 - sp_size[1] // 4 * 9), 'да', (0, 0, 0), font=sp_font)
        draw.text((dots['D'][0], imge_size[1] // 2 - sp_size[1] // 4 * 9), 'нет', (0, 0, 0), font=sp_font)

        draw.text((imge_size[0] // 2 - text_width // 2, imge_size[1] // 2 - text_height // 2 - 4),
                  block_info['item'], (0, 0, 0), font=font)


        # рисуем внутрености
        insaid_code_img = draw_block_diagram(block_info['insaid_code'])
        arrow_img_1 = drow_arrow()

        nev_img = Image.new('RGB',
                            (max(img.width, insaid_code_img.width) + 80,
                             img.height + insaid_code_img.height + arrow_img_1.height + 20),
                            (255, 255, 255))

        nev_img.paste(arrow_img_1, ((nev_img.width - arrow_img_1.width) // 2, img.height))
        nev_img.paste(img, ((nev_img.width - img.width) // 2, 0))
        nev_img.paste(insaid_code_img, ((nev_img.width - insaid_code_img.width) // 2, img.height + arrow_img_1.height))

        draw = ImageDraw.Draw(nev_img)

        draw.text(((nev_img.width - arrow_img_1.width) // 2 + arrow_img_1.width, img.height),
                  'да', (0, 0, 0), font=sp_font)

        dots = [
            (nev_img.width // 2, img.height + arrow_img_1.height + insaid_code_img.height,),
            (nev_img.width // 2, img.height + arrow_img_1.height + insaid_code_img.height + 10,),
            (20, img.height + arrow_img_1.height + insaid_code_img.height + 10,),
            (20, img.height // 2,),
            ((nev_img.width - img.width) // 2, img.height // 2,),
        ]

        self._draw_lines(dots, draw)

        dots = [
            ((nev_img.width + img.width) // 2, img.height // 2,),
            (nev_img.width - 20, img.height // 2,),
            (nev_img.width - 20, nev_img.height,),
            (nev_img.width // 2, nev_img.height,),
        ]

        self._draw_lines(dots, draw)

        return nev_img

    def type_if(self, simplified_if_else, font_name='arial.ttf', size=DEFAULT_SIZE, indent=20):
        font = ImageFont.truetype(font_name, size)
        sp_font = ImageFont.truetype(font_name, size // 4 * 3)
        if simplified_if_else['condition'] is None:
            return
        text_width, text_height = font.font.getsize(simplified_if_else['condition'])[0]
        sp_size = sp_font.font.getsize('нет')[0]

        imge_size = (max(text_width * 2, 60) + sp_size[0] * 2, max(int(text_height * 2.6), 20))

        dots = {
            'A': (max(text_width * 2, 60) // 2 + sp_size[0], 1,),
            'B': (sp_size[0], imge_size[1] // 2,),
            'C': (max(text_width * 2, 60) // 2 + sp_size[0], max(int(text_height * 2.6), 20) - 2,),
            'D': (max(text_width * 2, 60) + sp_size[0], imge_size[1] // 2 + 1,),
            'T': (max(text_width * 2, 60) + sp_size[0] * 2, imge_size[1] // 2 + 1,),
            'F': (0, imge_size[1] // 2,),
        }
        img = Image.new("RGB", imge_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.line((*dots['A'], *dots['B']), fill=(0, 0, 0), width=2)
        draw.line((*dots['B'], *dots['C']), fill=(0, 0, 0), width=2)
        draw.line((*dots['C'], *dots['D']), fill=(0, 0, 0), width=2)
        draw.line((*dots['D'], *dots['A']), fill=(0, 0, 0), width=2)

        draw.line((*dots['T'], *dots['D']), fill=(0, 0, 0), width=2)
        draw.line((*dots['F'], *dots['B']), fill=(0, 0, 0), width=2)

        draw.text((0, imge_size[1] // 2 - sp_size[1] // 4 * 9), 'нет', (0, 0, 0), font=sp_font)
        draw.text((dots['D'][0], imge_size[1] // 2 - sp_size[1] // 4 * 9), 'да', (0, 0, 0), font=sp_font)

        draw.text((imge_size[0] // 2 - text_width // 2, imge_size[1] // 2 - text_height // 2),
                  simplified_if_else['condition'], (0, 0, 0), font=font)

        # рисуем внутрености
        insaid_code_if_img = draw_block_diagram(simplified_if_else['true'])
        if type(simplified_if_else['false']) == dict:
            insaid_code_else_img = self.type_if(simplified_if_else['false'])
        elif simplified_if_else['false']:
            insaid_code_else_img = draw_block_diagram(simplified_if_else['false'])
        else:
            insaid_code_else_img = Image.new('RGB', (0, 0), (255, 255, 255))
        arrow_img = drow_arrow(lomg=20 + img.height // 2)

        nev_img = Image.new('RGB',
                            (max(img.width, max(insaid_code_if_img.width, insaid_code_else_img.width) * 2) + indent * 4,
                             img.height + max(insaid_code_if_img.height, insaid_code_else_img.height) + indent * 2),
                            (255, 255, 255))

        draw = ImageDraw.Draw(nev_img)

        nev_img.paste(img, ((nev_img.width - img.width) // 2, 0))

        nev_img.paste(arrow_img, (nev_img.width - insaid_code_if_img.width // 2, img.height // 2))
        draw.line(((nev_img.width + img.width) // 2, img.height // 2,
                   nev_img.width - insaid_code_if_img.width // 2 + 4, img.height // 2,), fill=(0, 0, 0), width=2)

        nev_img.paste(insaid_code_if_img, (nev_img.width - insaid_code_if_img.width, img.height + indent))

        dots = [
            (nev_img.width - insaid_code_if_img.width // 2 + 4, img.height + indent + insaid_code_if_img.height,),
            (nev_img.width - insaid_code_if_img.width // 2 + 4, nev_img.height,),
            (nev_img.width // 2, nev_img.height,),
        ]
        self._draw_lines(dots, draw)

        if insaid_code_else_img.size != (0, 0):
            nev_img.paste(arrow_img, (insaid_code_else_img.width // 2, img.height // 2))
            nev_img.paste(insaid_code_else_img, (0, img.height + indent))
            draw.line((insaid_code_else_img.width // 2 + 4, img.height // 2,
                       (nev_img.width - img.width) // 2, img.height // 2,), fill=(0, 0, 0), width=2)
            dots = [
                (insaid_code_else_img.width // 2, img.height + insaid_code_else_img.height + indent,),
                (insaid_code_else_img.width // 2, nev_img.height - 1,),
                (nev_img.width // 2, nev_img.height - 1,),
            ]
            self._draw_lines(dots, draw)
        else:
            dots = [
                ((nev_img.width - img.width) // 2, img.height // 2,),
                ((nev_img.width - img.width) // 2, nev_img.height - 1,),
                (nev_img.width // 2, nev_img.height - 1,),
            ]
            self._draw_lines(dots, draw)

        # nev_img.show()
        return nev_img

    def _drow_ends(self, insaid_code, ends=('начало', 'конец'), font='arial.ttf', size=DEFAULT_SIZE):
        img_begin = self.type_ends(ends[0])
        img_end = self.type_ends(ends[1])

        # рисуем внутрености
        insaid_code_img = draw_block_diagram(insaid_code)
        arrow_img_1 = drow_arrow()

        nev_img = Image.new('RGB',
                            (max(img_begin.width, insaid_code_img.width) + 80,
                             img_begin.height + insaid_code_img.height + arrow_img_1.height * 2 + img_end.height),
                            (255, 255, 255))

        nev_img.paste(arrow_img_1, ((nev_img.width - arrow_img_1.width) // 2, img_begin.height))
        nev_img.paste(img_begin, ((nev_img.width - img_begin.width) // 2, 0))
        nev_img.paste(arrow_img_1, ((nev_img.width - arrow_img_1.width) // 2,
                                    img_begin.height + insaid_code_img.height + arrow_img_1.height))
        nev_img.paste(insaid_code_img, ((nev_img.width - insaid_code_img.width) // 2,
                                        img_begin.height + arrow_img_1.height))
        nev_img.paste(img_end, ((nev_img.width - img_end.width) // 2,
                                img_begin.height + insaid_code_img.height + arrow_img_1.height * 2))
        return nev_img

    def type_defld_code(self, code):
        return self._drow_ends(code)

    def type_def(self, code):
        return self._drow_ends(code['insaid_code'], ends=(f'начало: {code['item']}', f'конец: {code['item']}'))


# img.save('rectangle_with_text.png')


# PaintBlock().type_if("'e5gks").show('charimg')

def drow_arrow(lomg=20, width=3):
    img_arrow = Image.new('RGB', (width * 3, lomg), (255, 255, 255))

    draw = ImageDraw.Draw(img_arrow)

    draw.line((width * 3 // 2, 0, width * 3 // 2, lomg), fill=(0, 0, 0), width=2)
    draw.polygon([(width * 3 // 2, lomg), (0, lomg - width), (width * 3, lomg - width)], fill=(0, 0, 0))
    return img_arrow


def draw_block_diagram(code):
    image_block_diagram = Image.new('RGB', (0, 0), (255, 255, 255))
    height = 0
    len_code = len(code)

    for i in range(len_code):
        element = code[i]

        # if element['insaid_code']:
        #     draw_blck_diagram(element['insaid_code']).show('charimg')

        if element['type'] in PaintBlock().function_library.keys():
            image_from_element = PaintBlock().function_library[element['type']](element)

        block_diagram_size = list(image_block_diagram.size)
        elem_image_size = list(image_from_element.size)

        block_diagram_size[0] = max(elem_image_size[0], block_diagram_size[0])

        img_arrow = drow_arrow()
        arrow_image_size = list(img_arrow.size)

        if i == len_code - 1:
            arrow_image_size[1] = 0

        nev_image = Image.new('RGB',
                              (block_diagram_size[0],
                               elem_image_size[1] + block_diagram_size[1] + arrow_image_size[1]),
                              (255, 255, 255))
        nev_image.paste(image_block_diagram, ((nev_image.width - image_block_diagram.width) // 2, 0))

        image_block_diagram = nev_image
        image_block_diagram.paste(image_from_element, ((block_diagram_size[0] - elem_image_size[0]) // 2, height))

        height += image_from_element.height

        image_block_diagram.paste(img_arrow, ((block_diagram_size[0] - arrow_image_size[0]) // 2, height))

        height += arrow_image_size[1]
    return image_block_diagram
