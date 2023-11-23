import constants

import pprint


class Block():
    IS_USE_TABS = False

    def __init__(self):
        pass

    def get_nesting(self, texst):
        if self.IS_USE_TABS:
            texst = texst.replace('\t', '    ')
        return (len(texst) - len(texst.lstrip())) // 4

    def decoder(self, code, nesting=0):
        code_blocs = []

        for i in range(len(code)):
            item = code[i]
            stript_item = item.strip()

            insaid_code = None

            if not len(stript_item) or stript_item[0] == '#':
                continue

            if stript_item[-1] == ':':
                insaid_code = self.decoder(code[i + 1:], nesting=nesting + 1)

            if self.get_nesting(item) < nesting:
                return code_blocs

            if self.get_nesting(item) == nesting:
                block_info = self.get_block_info(stript_item)
                block_info['insaid_code'] = insaid_code
                code_blocs.append(block_info)

        return code_blocs

    def get_block_info(self, block):
        block_info = {
            'item': None,
            'type': None,
            'insaid_code': None,
        }

        for key in constants.BLOCKS_WITH_ATTACHMENT_ID.keys():
            if block[:len(key)] == key:
                block_info['item'] = block[len(key) + 1:-1]
                block_info['type'] = constants.BLOCKS_WITH_ATTACHMENT_ID[key]
                return block_info
        else:
            if 'input' in block:
                block_info['item'] = block
                block_info['type'] = constants.SPECIAL_BLOCKS_ID['input']
            elif block[:5] == 'print':
                block_info['item'] = block[5:]
                block_info['type'] = constants.SPECIAL_BLOCKS_ID['print']
            else:
                block_info['item'] = block
                block_info['type'] = constants.SPECIAL_BLOCKS_ID['none type']
        return block_info


if __name__ == '__main__':
    f = open('test')
    code = f.readlines()
    q = Block().decoder(code)
    print('\n\n\n\n\n\n')
    print(pprint.pformat(q))
