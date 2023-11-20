f = open('test')

'''
2 = блок кода
4 = вайл
8 = фор
16 = иф
32 = елив
64 = елсе
'''


def col_spasess(string):
    ansver = 0
    for i in string:
        if i != ' ':
            break
        ansver += 1
    return ansver // 2


def get_insaid_code(code, nesting):
    nesting += 1
    insaid_code = []

    for i in code:
        if i.strip() == '':
            continue
        if col_spasess(i) < nesting:
            return insaid_code
        insaid_code.append(i)



def decoder(code, nesting=0):
    code_blocs = []
    continuer = 0
    for i in range(len(code)):
        if continuer > 0:
            continuer -= 1
            continue
        item = {
            'tupe': None,
            'content': None,
            'insaid code': None,
        }
        if code[i].strip() == '':
            continue

        ii = code[i].lstrip()
        if ii[:2] == 'if':

            item['tupe'] = 16
            item['content'] = code[i]
            insaid_code = get_insaid_code(code[i + 1:], nesting)
            print(insaid_code, code[i + 1:], nesting)
            continuer = len(insaid_code)
            item['insaid code'] = decoder(insaid_code, nesting=nesting + 1)
        else:
            item['tupe'] = 2
            item['content'] = code[i]
        code_blocs.append(item)
    return code_blocs


import pprint

if __name__ == '__main__':
    code = f.readlines()
    print(pprint.pformat(decoder(code)))
