from PIL import Image, ImageDraw, ImageFont

# создаем изображение
img = Image.new('RGB', (200, 200), color='white')

# получаем доступ к объекту ImageDraw
draw = ImageDraw.Draw(img)

# задаем размер шрифта и выбираем шрифт
font_size = 20
font = ImageFont.truetype("arial.ttf", font_size)

# рисуем текст
text = "Hello, world!"
draw.text((50, 50), text, fill='black', font=font)

draw.rectangle(50, 50, int(len(text)) * 2 + 1, int(len(text)) * 2 + 1, outline='black')
# сохраняем изображение
img.save('text.png')