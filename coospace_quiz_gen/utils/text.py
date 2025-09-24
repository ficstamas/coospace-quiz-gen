def dedent(s):
    return ''.join([m.lstrip() for m in s.split('\n')]).replace("\n", "")