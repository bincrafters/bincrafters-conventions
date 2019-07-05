# -*- coding: utf-8 -*-

import ast


class CheckToolsGetVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.matches = []

    def visit_Call(self, node):
        def check_node(node):
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.value.id != "tools" or node.func.attr != "get":
                    return
                sha256 = False
                for kw in node.keywords:
                    if kw.arg == 'sha256':
                        sha256 = True
                self.matches.append({"sha256": sha256, "lineno": node.lineno, "col_offset": node.col_offset})
        check_node(node)
        self.generic_visit(node)


def check_for_download_hash(main, file):
    conanfile = open(file, "r")
    recipe = conanfile.read()
    conanfile.close()

    v = CheckToolsGetVisitor()
    n = ast.parse(recipe)
    v.visit(n)

    if not v.matches:
        main.output_result_check(passed=True, skipped=True, title="SHA256 hash in tools.get()", reason="tools.get() isn't used")
        return True

    for match in v.matches:
        if match["sha256"]:
            main.output_result_check(passed=True, title="SHA256 hash in tools.get()")
        else:
            main.output_result_check(passed=False, title="SHA256 hash in tools.get()",
                                     reason="checksum not found ({file}:{line})".format(file=file, line=match["lineno"]))
    return all(m["sha256"] for m in v.matches)
