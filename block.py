import constants


class Block():
    IS_USE_TABS = False
    END_BLOCK_WITH_ATTACHMENT = ':'

    def __init__(self):
        pass

    def _de_contain(self, container_if):
        print('_de_contain')
        simplified_if_else = {
            'type': 4,
            'condition': None,
            'true': None,
            'false': None,
        }
        if len(container_if) == 1:
            simplified_if_else['condition'] = container_if[0]['item']
            simplified_if_else['true'] = container_if[0]['insaid_code']
        elif len(container_if) == 2:
            simplified_if_else['condition'] = container_if[0]['item']
            simplified_if_else['true'] = container_if[0]['insaid_code']
            if container_if[1]['type'] == 8:
                simplified_if_else['false'] = self._de_contain(container_if[1:])
            elif container_if[1]['type'] == 16:
                simplified_if_else['false'] = container_if[1]['insaid_code']
        else:
            simplified_if_else['condition'] = container_if[0]['item']
            simplified_if_else['true'] = container_if[0]['insaid_code']
            simplified_if_else['false'] = self._de_contain(container_if[1:])
        return simplified_if_else

    def get_nesting(self, texst):
        if self.IS_USE_TABS:
            texst = texst.replace('\t', '    ')
        return (len(texst) - len(texst.lstrip())) // 4

    def decoder(self, code, nesting=0):
        code_blocs = []
        def_blocs = []
        condition_blocs = []

        for i in range(len(code)):
            item = code[i]
            stript_item = item.strip()

            insaid_code = None

            if not len(stript_item) or stript_item[0] == '#':
                continue

            if stript_item[-1] == self.END_BLOCK_WITH_ATTACHMENT:
                insaid_code = self.decoder(code[i + 1:], nesting=nesting + 1)

            if self.get_nesting(item) < nesting:
                if condition_blocs:
                    code_blocs.append(self._de_contain(condition_blocs))
                return code_blocs

            if self.get_nesting(item) == nesting:
                block_info = self.get_block_info(stript_item)
                block_info['insaid_code'] = insaid_code
                if block_info['type'] == 4:
                    if condition_blocs:
                        code_blocs.append(self._de_contain(condition_blocs))
                        condition_blocs = []
                    condition_blocs.append(block_info)
                elif 8 <= block_info['type'] <= 16:
                    condition_blocs.append(block_info)
                elif block_info['type'] == 2:
                    def_blocs.append(block_info)
                else:
                    if condition_blocs:
                        code_blocs.append(self._de_contain(condition_blocs))
                        condition_blocs = []
                    code_blocs.append(block_info)
        if condition_blocs:
            code_blocs.append(self._de_contain(condition_blocs))

        if nesting == 0:
            return code_blocs, def_blocs
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
                block_info['item'] = f'ввод: {block.split('=')[0].strip()}'
                block_info['type'] = constants.SPECIAL_BLOCKS_ID['input']
            elif block[:5] == 'print':
                block_info['item'] = f'вывод: {block[6:-1]}'
                block_info['type'] = constants.SPECIAL_BLOCKS_ID['print']
            else:
                block_info['item'] = block
                block_info['type'] = constants.SPECIAL_BLOCKS_ID['none type']
        return block_info


if __name__ == '__main__':
    import pprint

    f = open('test')
    code = f.readlines()
    q = Block().decoder(code)
    print('\n\n\n\n\n\n')
    print(pprint.pformat(q))
