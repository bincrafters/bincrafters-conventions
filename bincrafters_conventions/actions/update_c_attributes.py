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


def update_c_author(main, file):
    """ Update author tuple
    """

    conanfile = open(file).read()
    match = re.search("""author\\s*=\\s*(['"])(?P<author>.*)\\1""", conanfile)
    if match:
        original = match[0]
        name_mail = re.match('(?P<name>.*)\\s<(?P<mail>.*)>', match['author'])
        if name_mail:
            print(name_mail)
            print(repr(name_mail['name']))
            if name_mail['name'].lower() == 'bincrafters' and name_mail['name'] != 'Bincrafters':
                print('DD')
                change = 'author = {m}{n} <{e}>{m}'.format(
                    m=match[1], n=name_mail['name'].capitalize(), e=name_mail['mail'].lower())
                main.replace_in_file(file, original, change)
                return True
    return False
