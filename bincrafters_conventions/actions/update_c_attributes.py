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

        main.output_result_update("Put parentheses around topics")
        main.replace_in_file(file, original, change)
        return True
    return False


def update_c_delete_author(main, file):
    """ Remove author attribute if equals to Bincrafters or conan-community
    """

    updated = False
    content = ""

    with open(file) as ifd:
        for line in ifd:
            match = re.search("""author\\s*=\\s*(['"])(?P<author>.*)\\1""", line)
            if match:
                author = re.match('(?P<name>.*)\\s<(?P<mail>.*)>', match['author'])
                if (author and author['name'].lower() == 'bincrafters')\
                        or match['author'].lower() == "conan community":
                    main.output_result_update("Delete author attribute: {}".format(line.strip()))
                    updated = True
                else:
                    content += line
            else:
                content += line

    if updated:
        with open(file, 'w') as fd:
            fd.write(content)

    return updated
