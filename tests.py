def _de_contain(container_if):
    q = {
        'condition': None,
        'true': None,
        'false': None,
    }
    if len(container_if) == 2 and container_if[1][0] is None:
        q['condition'] = container_if[0][0]
        q['true'] = container_if[0][1]
        q['false'] = container_if[1][1]
        return q
    elif len(container_if) >= 2:
        q['condition'] = container_if[0][0]
        q['true'] = container_if[0][1]
        q['false'] = _de_contain(container_if[1:])
        return q
    q['condition'] = container_if[0][0]
    q['true'] = container_if[0][1]
    return q


t = [['2 > 3', '43'], ['2 > 3', '43'], ['2 > 3', '43']]
print(_de_contain(t))
t = [['2 > 3', '43'], [None, '1']]
print(_de_contain(t))