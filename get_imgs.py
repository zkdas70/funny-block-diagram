import block, draw_block_diagram
from io import BytesIO
from PIL.ImageQt import ImageQt


def get_imgs(file_path):
    # :param file_path: папка с файлом
    # :return: вернет список из элементов (img_bytes, name)

    block_diagrams = []

    with open(file_path) as f:
        file_code = f.readlines()

    decodet_file_code = block.Block().decoder(file_code)
    img_bytes = BytesIO()
    image = draw_block_diagram.PaintBlock().type_defld_code(decodet_file_code[0])

    image.save(img_bytes, format='JPEG')

    block_diagrams.append((img_bytes, 'основной код программы'))

    for function_code in decodet_file_code[1]:
        img_bytes = BytesIO()
        image = draw_block_diagram.draw_block_diagram([function_code])

        image.save(img_bytes, format='JPEG')

        block_diagrams.append((img_bytes, function_code['item']))

    return block_diagrams
