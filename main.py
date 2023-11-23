import pprint

f = open('test')


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

        if not len(stript_item):
            continue

        if stript_item[-1] == ':':
            insaid_code = decoder(code[i + 1:], nesting=nesting + 1)

        if get_nesting(item) < nesting:
            return code_blocs

        if get_nesting(item) == nesting:
            code_blocs.append((stript_item, insaid_code))

    return code_blocs


if __name__ == '__main__':
    code = f.readlines()
    q = decoder(code)
    print('\n\n\n\n\n\n')
    print(pprint.pformat(q))
