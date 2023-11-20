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


def decoder(code, nesting=0, continuer=0):
    code_blocs = []

    for i in range(len(code)):
        item = code[i]
        stript_item = item.strip()

        if stript_item == '':
            continue
        if get_nesting(item) < nesting:
            return code_blocs
        if continuer:
            continuer -= 1
            continue

        insaid_code = None
        if stript_item[-1] == ':':
            insaid_code = decoder(code[i + 1:], nesting=nesting + 1, continuer=continuer)
            continuer += len(insaid_code)
            #print(code[i + 1:])

        code_blocs.append([stript_item, insaid_code])

    return code_blocs


import pprint

if __name__ == '__main__':
    code = f.readlines()
    q = decoder(code)
    print('\n\n\n\n\n\n')
    print(pprint.pformat(q))
