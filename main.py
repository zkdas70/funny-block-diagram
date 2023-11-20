f = open('test')

'''
2 = блок кода
4 = вайл
8 = фор
16 = иф
32 = елив
64 = елсе
'''


def get_nesting(string):
    nesting = 0
    for i in string:
        if i != ' ':
            break
        nesting += 1
    return nesting // 2


def decoder(code, nesting=0):
    code_blocs = []
    continuer = 0
    for i in range(len(code)):
        item = code[i]
        stript_item = item.strip()

        if stript_item == '':
            continue
        if continuer:
            continuer -= 1
            continue
        if get_nesting(item) < nesting:
            return code_blocs

        insaid_code = None
        if stript_item[-1] == ':':
            insaid_code = decoder(code[i + 1:], nesting=nesting + 1)
            continuer += len(insaid_code)

        code_blocs.append([stript_item, insaid_code, nesting])

    return code_blocs


import pprint

if __name__ == '__main__':
    code = f.readlines()
    print(pprint.pformat(decoder(code)))
