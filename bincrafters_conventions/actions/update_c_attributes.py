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


def update_c_delete_licensemd_export(main, file):
    """ Remove export of LICENSE.md
    """

    updated = False
    content = ""

    complete = ['exports = ["LICENSE.md"]', "exports = ['LICENSE.md']"]
    incomplete = ['exports = ["LICENSE.md", ', "exports = ['LICENSE.md', ", 'exports = ["LICENSE.md",',
                  "exports = ['LICENSE.md',"]

    with open(file) as ifd:
        for line in ifd:
            updated_line = False
            if not updated:
                for pattern in complete:
                    if line.strip() == pattern:
                        updated = True
                        updated_line = True
                        break

            if not updated:
                for pattern in incomplete:
                    if line.strip().startswith(pattern):
                        content += line.replace(pattern, "exports = [")
                        updated = True
                        updated_line = True
                        break

            if not updated_line:
                content += line

    if updated:
        main.output_result_update("Delete export of LICENSE.md file")
        with open(file, 'w') as fd:
            fd.write(content)

    return updated
