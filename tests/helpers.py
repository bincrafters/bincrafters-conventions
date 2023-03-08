
import tempfile
import os
from shutil import copyfile


def prepare_old_file(file_name: str, suffix: str, file_target_name: str = "", old: str = "", expected: str = ""):
    if old == "":
        old = file_name + "_old"

    if expected == "":
        expected = file_name + "_expected"

    if file_target_name == "":
        file_target_name = old

    tmp_dir = tempfile.mkdtemp(prefix=old)  # , suffix=suffix

    test_file_src = os.path.join("files", f"{old}{suffix}")
    expected_file_src = os.path.join("files", f"{expected}{suffix}")
    target_test_file = os.path.join(tmp_dir, f"{file_target_name}{suffix}")
    target_expected_file = os.path.join(tmp_dir, f"{expected}{suffix}")

    copyfile(test_file_src, target_test_file)
    copyfile(expected_file_src, target_expected_file)

    return target_test_file, target_expected_file


def compare_file(path_old: str, expected_path: str):
    """ This is needed to ignore different line endings styles
        e.g. filecmp.cmp would throw an error with different line ending
    """
    l1 = l2 = True
    with open(path_old, 'r') as f1, open(expected_path, 'r') as f2:
        while l1 and l2:
            l1 = f1.readline()
            l2 = f2.readline()
            if l1 != l2:
                print("Does not match:")
                print(l1)
                print(l2)
                return False
    return True
