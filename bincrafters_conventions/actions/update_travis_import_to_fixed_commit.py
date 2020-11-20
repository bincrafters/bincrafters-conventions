def update_travis_import_to_fixed_commit(main, travis_file) -> bool:
    """
    We deprecated Travis config files and will remove eventually existing importable config files.
    Let's replace references to the former master branch, or the current main branch with a fixed commit
    so that the CI runs don't break even after removal of the files from the main branch.

    :param travis_file: file path to a Travis config file
    :return:
    """
    if main.replace_in_file(
            travis_file,
            "bincrafters/templates:.ci/travis-macos.yml@master",
            "bincrafters/templates:.ci/travis-macos.yml@12f4883f65fcbc521d7425636083ce9bba4be5cd")\
        or main.replace_in_file(
            travis_file,
            "bincrafters/templates:.ci/travis-macos.yml@main",
            "bincrafters/templates:.ci/travis-macos.yml@12f4883f65fcbc521d7425636083ce9bba4be5cd")\
        or main.replace_in_file(
            travis_file,
            "bincrafters/templates:.ci/travis-macos-installer.yml@master",
            "bincrafters/templates:.ci/travis-macos-installer.yml@12f4883f65fcbc521d7425636083ce9bba4be5cd")\
        or main.replace_in_file(
            travis_file,
            "bincrafters/templates:.ci/travis-macos-installer.yml@main",
            "bincrafters/templates:.ci/travis-macos-installer.yml@12f4883f65fcbc521d7425636083ce9bba4be5cd"):
        main.output_result_update(title="CI: Update Travis config import to fixed hash.")
        return True

    return False
