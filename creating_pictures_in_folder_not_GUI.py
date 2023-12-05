import draw_block_diagram, block

import os, shutil

FOLDER_PATH = 'not gui' # указываем путь к папке

FOLDER_NAMES = {
    'input':'input', # имя папки для считывания файлов
    'output': 'output', # имя папки для вывода
}

if os.path.exists(f'{FOLDER_PATH}/{FOLDER_NAMES['output']}'):
    shutil.rmtree(f'{FOLDER_PATH}/{FOLDER_NAMES['output']}')

for name in FOLDER_NAMES.values():
    path = f'{FOLDER_PATH}/{name}'
    if not os.path.exists(path):
        os.makedirs(path)

files = os.listdir(f'{FOLDER_PATH}/{FOLDER_NAMES['input']}')
for file in files:
    with open(f'{FOLDER_PATH}/{FOLDER_NAMES['input']}/{file}') as f:
        file_code = f.readlines()
    decodet_file_code = block.Block().decoder(file_code)

    img = draw_block_diagram.PaintBlock().type_defld_code(decodet_file_code[0])
    img.save(f'{FOLDER_PATH}/{FOLDER_NAMES['output']}/{file.split('.')[0]}_cobe.png')

    for i in range(len(decodet_file_code[1])):
        img = draw_block_diagram.draw_block_diagram([decodet_file_code[1][i]])
        img.save(f'{FOLDER_PATH}/{FOLDER_NAMES['output']}/{file.split('.')[0]}_{decodet_file_code[1][i]['item']}.png')


