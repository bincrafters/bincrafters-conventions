import re


def update_c_topics(main, file):
    """ Update topics tuple
    """

    conanfile = open(file).read()
    match = re.search("""topics\\s*=\\s*(?P<topics>.*)""", conanfile)
    if match:
        original = match[0]
        if match['topics'][0] == '(':
            return False
        topics = match['topics']

        topics_iter = re.finditer('''(['"])(\\S*)\\1''', topics)
        change = 'topics = ({})'.format(', '.join('{}{}{}'.format(t[1], t[2], t[1]) for t in topics_iter))

        main.replace_in_file(file, original, change)
        return True
    return False
