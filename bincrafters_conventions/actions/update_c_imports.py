import re

def update_c_imports(main, file):
    """ This updates the imports a ConanFile uses.
        It can only updates imports when it can update the corresponding usage (in other updates) as well.

        :param file: Conan file path
    """

    updated = False

    imports = {}
    # Schema:
    #
    #   first line: from original_X import original_Y -> ("original_X", "original_Y")
    #   second line: from updated_X import updated_Y -> ("updated_X", "updated_Y")
    #   third line: ("min Conan version the new import works", "first Conan version the new import BREAKS, doesn't work anymore, add * if there is no such version yet")
    # for the imported symbols:
    #
    #  * is both a literal * from imports, but also telling the script to just leave unchaged whatever was imported; useful for just changing from where you import
    #
    # Another example, updating an import in the form of
    #   import os
    # to 
    #   import shiny_new_os
    # can be archived with
    #   [("*", "os"), ("*", "shiny_new_os"), ("*", "*")]
    #

    imports_updates_conan = [
        # Conan 1.15
        [
            ("conans.model.version", "Version"),
            ("conans.tools", "Version"),
            ("1.15.0", "2.0.0")
        ],
        [
            ("conans.model.version", "Version"),
            ("conan.tools.scm", "Version"),
            ("1.46.0", "*")
        ],
        # Conan Version unknown FIXME
        [
            ("conans", "ConanFile"),
            ("conan", "ConanFile"),
            ("FIXME", "*")
        ],
        # Conan 1.46
        [
            ("conans.tools", "Version"),
            ("conan.tools.scm", "Version"),
            ("1.46.0", "*")
        ],
        # Conan 1.47
        [
            ("conans.errors", "*"),
            ("conan.errors", "*"),
            ("1.47.0", "*")
        ]
    ]
    imports_namespace_order = [
        "conan",
        "conan.errors",
        "conan.tools.microsoft",
        "conan.tools.files",
        "conan.tools.build",
        "conan.tools.scm",
        "conan.tools.cmake",
        "conan.tools.env",
        "conans",
        "conans.tools",
    ]
    keywords_import_lines = {
        "from",
        "import"
    }
    keywords_import_conan_lines = {
        "from conan" # this implicits from conans
    }
    keywords_stop_lines = {
        "def",
        "class",
        "with",
    }
    keywords_ignore_lines = {
        '"', # comments
        '#', # comments
    }


    def _sanitize_line(line_input: str):
        # Whitespaces
        line_input = line_input.strip()
        # Newlines: good idea?
        # line_input = line_input.strip('\n')
        # Single l FIXME: logical lines broken into multiples
        # line_input = line_input.strip("\")
        return line_input

    def _is_import_line(line_input: str) -> bool:
        for keyword in keywords_import_lines:
            if line_input.startswith(keyword):
                return True

        return False

    def _is_import_conan_line(line_input: str) -> bool:
        for keyword in keywords_import_conan_lines:
            if line_input.startswith(keyword):
                return True

        return False

    def _split_several_imports_in_list(symbols: str) -> list:
        res = symbols.split(",")
        return [sym.strip() for sym in res]


    new_conanfile = ""
    with open(file, encoding="utf-8") as cf:
        for original_line in cf.readlines():
            line = _sanitize_line(original_line)

            if _is_import_line(line):
                print(line)
                p1 = re.fullmatch("from (.+) import (.+)", line)
                if p1:
                    namespace = p1.group(1)
                    imported_symbols = p1.group(2)
                    if not namespace in imports:
                        imports[namespace] = []

                    for symb in _split_several_imports_in_list(imported_symbols):
                        if not symb in imports[namespace]:
                            imports[namespace].append(symb)

                else:
                    p2 = re.fullmatch("import (.+)", line)
                    if p2:
                        namespace = p2.group(1)
                        if not "*" in imports:
                            imports["*"] = []

                        for symb in _split_several_imports_in_list(namespace):
                            if not symb in imports["*"]:
                                imports["*"].append(symb)
            else:
                new_conanfile += original_line

    print("")
    print("read:")
    print("")
    print(imports)

    for iuc in imports_updates_conan:
        namespace, symbol = iuc[0]
        if namespace in imports:
            if symbol == "*":
                # This is for update rules that update the namespace, but don't care which symbols are imported; just take all symbols to the new namespace
                new_namespace, _ = iuc[1]
                if not new_namespace in imports:
                    imports[new_namespace] = []
            
                for symb in imports[namespace]:
                    imports[namespace].remove(symb)
                    if not symb in imports[new_namespace]:
                        imports[new_namespace].append(symb)

                    main.output_result_update(title=f"Update import: {namespace};{symb} -> {new_namespace};{symb}")
                    updated = True

            elif symbol in imports[namespace]:
                imports[namespace].remove(symbol)

                # print(f"{symbol} is in imports namespace for {namespace}")
                new_namespace, new_symbol = iuc[1]
                if not new_namespace in imports:
                    imports[new_namespace] = []

                if not new_symbol in imports[new_namespace]:
                    imports[new_namespace].append(new_symbol)

                main.output_result_update(title=f"Update import: {namespace};{symbol} -> {new_namespace};{new_symbol}")
                updated = True

    if not updated:
        return False

    print("")
    print("updated:")
    print("")
    print(imports)

    # Sanitize new imports
    # remove namespace that don't have any symbols to import left
    delete_namespaces = []
    for namespace, symbols in imports.items():
        if symbols == []:
            delete_namespaces.append(namespace)
    for namespace in delete_namespaces:
        del imports[namespace]

    # Order the imports
    ordered_imports = {}
    for namespace in imports_namespace_order:
        if namespace in imports:
            ordered_imports[namespace] = imports[namespace]
    for namespace in imports:
        if not namespace in ordered_imports:
            ordered_imports[namespace] = imports[namespace]
    imports = ordered_imports
    # Move import X statements to the end
    imports["*"] = imports.pop("*")

    print("")
    print("sanitized:")
    print("")
    print(imports)

    # Generate new import code lines
    new_import_lines = ""
    for namespace, symbols in imports.items():
        if namespace == "*":
            for symb in symbols:
                new_import_lines += f"import {symb}\n"
        else:
            if len(symbols) == 1:
                new_import_lines += f"from {namespace} import {symbols[0]}\n"
            else:
                new_symbols = ", ".join(symbols)
                new_import_lines += f"from {namespace} import {new_symbols}\n"


    with open(file, "w", encoding="utf-8") as fd:
        fd.write(new_import_lines + new_conanfile)

    return True
