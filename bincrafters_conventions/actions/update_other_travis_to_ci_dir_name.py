import shutil
import os


def update_other_travis_to_ci_dir_name(main):
    """ Replace Travis directory by CI dir
    """
    travis_dir = ".travis/"
    ci_dir = ".ci/"
    if os.path.isdir(travis_dir):
        shutil.move(os.path.abspath(travis_dir), os.path.abspath(ci_dir))
        main.output_result_update("Update Travis directory path from .travis -> .ci")
        return True
    return False
