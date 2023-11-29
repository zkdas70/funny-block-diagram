from PIL import Image, ImageDraw

# Создаем изображение и объект ImageDraw
image = Image.new('RGB', (300, 300), color='white')
draw = ImageDraw.Draw(image)

# Определяем координаты вершин треугольника
points = [(100, 100), (200, 100), (150, 200)]

# Рисуем треугольник
draw.polygon(points, fill='red')

# Сохраняем изображение
image.save('triangle.png')
