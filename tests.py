def decoder(code):
    lines = code.split('\n')
    deco = []
    tab_count = 0
    current_line = ''
    for i, line in enumerate(lines):
        if line.strip() != '':
            current_tab_count = line.count('\t')
            if current_tab_count > tab_count:
                current_line += line.strip() + ' '
            else:
                if i == len(lines) - 1:
                    deco.append([current_line, '', ''])
                    current_line = ''
                else:
                    deco.append([current_line, decoder('\n'.join(lines[i:])), ''])
                    current_line = ''
            tab_count = current_tab_count
    return deco


# пример использования
code = ("if len(a) <= 2:\n"
        "\tprint('if')\n"
        "print('end')")
decoded_code = decoder(code)
print(decoded_code)