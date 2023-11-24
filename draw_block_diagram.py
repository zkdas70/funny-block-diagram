from PIL import Image, ImageDraw

test = [{'insaid_code': None,
         'item': "n = int(input('РІРІРµРґРёС‚Рµ n'))",
         'type': 128},
        {'insaid_code': None, 'item': 'divider = 0', 'type': 512},
        {'insaid_code': None, 'item': 'dividend = 0', 'type': 512},]

# Создаем изображение размером 300x300 пикселей
image = Image.new('RGB', (300, 300), color='white')

# Создаем объект для рисования на изображении
draw = ImageDraw.Draw(image)

# Рисуем прямоугольник
draw.rectangle((50, 50, 200, 200), outline='black')

# Рисуем текст
text = 'Hello, world!'
draw.text((100, 100), text, fill='red')

# Сохраняем изображение в файл
image.save('image.png')


def painter(block_info):
    pass