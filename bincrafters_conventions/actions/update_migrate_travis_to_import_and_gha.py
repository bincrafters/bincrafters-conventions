import os
import shutil
from bincrafters_conventions.actions.update_gha import update_gha


def update_migrate_travis_to_import_and_gha(main, travis_file) -> bool:
    def _contains(search_pattern: str) -> bool:
        return main.file_contains(travis_file, search_pattern)

    runs_macos = _contains("CONAN_APPLE_CLANG_VERSIONS")
    workflow_file = os.path.join(os.path.dirname(travis_file), ".github", "workflows", "conan.yml")

    def _update_travis(file_name: str) -> None:
        if runs_macos:
            shutil.copy(os.path.join(os.path.dirname(__file__), file_name),
                    travis_file)
            main.output_result_update(title="CI: Travis config migrated to import template")
        else:
            os.remove(travis_file)
            main.output_result_update(title="CI: Delete Travis config")

        for file in ["install.sh", "run.sh"]:
            file_path = os.path.join(os.path.dirname(travis_file), ".ci", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def _create_gha(file_name: str) -> None:
        os.makedirs(os.path.dirname(workflow_file), exist_ok=True)
        shutil.copy(os.path.join(os.path.dirname(__file__), file_name),
                    workflow_file)
        main.output_result_update(title="CI: Migrate Linux jobs from Travis to GitHub Actions")

    # Check if Travis config is already up to date; if so do nothing
    if _contains("import") and not _contains("install"):
        return False

    if not _contains("CONAN_CURRENT_PAGE"):
        _create_gha("travis_1_expected_gha.yml")
        _update_travis("travis_1_expected.yml")
    elif (_contains("CONAN_CURRENT_PAGE=2") or _contains("CONAN_CURRENT_PAGE=3") or _contains("CONAN_BUILD_TYPES"))\
            and not _contains("CONAN_CURRENT_PAGE=4"):
        _create_gha("travis_2_expected_gha.yml")
        _update_travis("travis_2_expected.yml")
    else:
        _create_gha("travis_2_expected_gha.yml")
        _update_travis("travis_3_expected.yml")

    update_gha(main, workflow_file)

    return True
