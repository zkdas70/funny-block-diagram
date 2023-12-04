t = {'condition': "__name__ == '__main__'", 'true': [{'item': 'ввод: n', 'type': 128, 'insaid_code': None}, {'item': 'm1 = imput_matrix(n=n, m=n)', 'type': 512, 'insaid_code': None}, {'item': 'm2 = imput_matrix(n=n, m=n)', 'type': 512, 'insaid_code': None}, {'item': "вывод: ('РїРѕР»СѓС‡РёР»Р°СЃСЊ РјР°С‚СЂРёС†Р°\\n' + get_ansver(m1, m2)", 'type': 256, 'insaid_code': None}], 'false': None}


def _de_contain(container_if):
    if type(container_if) == dict:
        return container_if
    simplified_if_else = {
        'condition': None,
        'true': None,
        'false': None,
    }
    if len(container_if) == 2 and container_if[1][0] is None:
        simplified_if_else['condition'] = container_if[0][0]
        simplified_if_else['true'] = container_if[0][1]
        simplified_if_else['false'] = container_if[1][1]
        return simplified_if_else
    elif len(container_if) >= 2:
        simplified_if_else['condition'] = container_if[0][0]
        simplified_if_else['true'] = container_if[0][1]
        simplified_if_else['false'] = _de_contain(container_if[1:])
        return simplified_if_else
    simplified_if_else['condition'] = container_if[0][0]
    simplified_if_else['true'] = container_if[0][1]
    return simplified_if_else

print(_de_contain(t))