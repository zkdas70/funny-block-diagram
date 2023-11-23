import pprint

f = open('test')


def get_block_info(block):
    BLOCK_ID = {
        'def': 2,
        'if': 4,
        'elif': 8,
        'else': 16,
        'for': 32,
        'while': 64,
        'input': 128,
        'print': 256,
        'none type' : 512,
    }

    block_info = {
        'item': None,
        'type': None,
        'insaid_code': None,
    }

    if block[:3] == 'def':
        block_info['item'] = block[4:-1]
        block_info['type'] = BLOCK_ID['def']
    elif block[:2] == 'if':
        block_info['item'] = block[3:]
        block_info['type'] = BLOCK_ID['if']
    elif block[:4] == 'elif':
        block_info['item'] = block[5:-1]
        block_info['type'] = BLOCK_ID['elif']
    elif block[:4] == 'else':
        block_info['item'] = block[5:-1]
        block_info['type'] = BLOCK_ID['else']
    elif block[:3] == 'for':
        block_info['item'] = block[4:-1]
        block_info['type'] = BLOCK_ID['for']
    elif block[:5] == 'while':
        block_info['item'] = block[6:-1]
        block_info['type'] = BLOCK_ID['while']
    elif 'input' in block:
        block_info['item'] = block
        block_info['type'] = BLOCK_ID['input']
    elif block[:5] == 'print':
        block_info['item'] = block[5:]
        block_info['type'] = BLOCK_ID['print']
    else:
        block_info['item'] = block
        block_info['type'] = BLOCK_ID['none type']
    return block_info


# def get_nesting(string):
#     nesting = 0
#     for i in string:
#         if i != ' ':
#             break
#         nesting += 1
#     return nesting // 4

def get_nesting(texst):
    return texst.count('    ')


def decoder(code, nesting=0):
    code_blocs = []

    for i in range(len(code)):
        item = code[i]
        stript_item = item.strip()

        insaid_code = None

        if not len(stript_item) or stript_item[0] == '#':
            continue

        if stript_item[-1] == ':':
            insaid_code = decoder(code[i + 1:], nesting=nesting + 1)

        if get_nesting(item) < nesting:
            return code_blocs

        if get_nesting(item) == nesting:
            block_info = get_block_info(stript_item)
            block_info['insaid_code'] = insaid_code
            code_blocs.append(block_info)

    return code_blocs


if __name__ == '__main__':
    code = f.readlines()
    q = decoder(code)
    print('\n\n\n\n\n\n')
    print(pprint.pformat(q))
