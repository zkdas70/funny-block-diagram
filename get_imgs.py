import block, draw_block_diagram
from PIL.ImageQt import ImageQt

def get_imgs(file_path):
    blocks_images = []

    with open(file_path) as f:
        file_code = f.readlines()

    decodet_file_code = block.Block().decoder(file_code)

    image = draw_block_diagram.PaintBlock().type_defld_code(decodet_file_code[0])

    blocks_images.append((ImageQt(image), 'основной код программы'))

    for i in range(len(decodet_file_code[1])):
        image = draw_block_diagram.draw_block_diagram([decodet_file_code[1][i]])

        blocks_images.append((ImageQt(image), decodet_file_code[1][i]['item']))
    return blocks_images

