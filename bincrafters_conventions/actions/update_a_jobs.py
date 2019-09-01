from .modules.jobs_update import update_add_new_compiler_versions


def update_a_jobs(main, file, compiler_versions: dict, images_mapping: dict, compiler_deleting: dict):
    """ This update script adds new compiler versions to the AppVeyor jobs

    :param file: CI file path
    :param compiler_versions: List of recommended new compiler versions
    :param images_mapping: Mapping of compiler version to specific CI runtime images
    :param compiler_deleting: Compiler versions which are getting deleted
    """

    platform = {
        "name": "AppVeyor",
        "beginning_keywords": ("matrix:",),
        "end_keyword": "install:",
        "delimiter": ": ",
        "job_beginning_indication": "-",
        "job_beginning_indication_use_spaces": False,
    }

    return update_add_new_compiler_versions(main, file, platform, compiler_versions, images_mapping, compiler_deleting)
