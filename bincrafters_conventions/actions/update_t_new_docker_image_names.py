def update_t_new_docker_image_names(main, file):
    """ Updates the names of the docker images from lasote to conanio
    """

    docker_mappings = {
        "lasote/conangcc49": "conanio/gcc49",
        "lasote/conangcc5": "conanio/gcc5",
        "lasote/conangcc6": "conanio/gcc6",
        "lasote/conangcc7": "conanio/gcc7",
        "lasote/conangcc8": "conanio/gcc8",
        "lasote/conanclang39": "conanio/clang39",
        "lasote/conanclang40": "conanio/clang40",
        "lasote/conanclang50": "conanio/clang50",
        "lasote/conanclang60": "conanio/clang60",
    }

    found_old_name = False

    for old, new in docker_mappings.items():
        if main.file_contains(file, old):
            main.replace_in_file(file, old, new)
            found_old_name = True

    if found_old_name:
        main.output_result_update(title="Travis: Update Docker image names from lasote/ to conanio/")
        return True

    return False
