def update_t_linux_image(main, file):
    """ Update the Travis Linux base image (i.e. native image, not the images we run via Docker)
    """

    image_update_mapping = {
        "sudo: required": "dist: xenial"
    }

    for old_image_version, new_image_version in image_update_mapping.items():
        if main.file_contains(file, old_image_version) and \
           not main.file_contains(file, new_image_version):
            if (main.replace_in_file(file, old_image_version, new_image_version)):
                main.output_result_update(title="Travis: Update Linux CI image from {} to {}".format(old_image_version, new_image_version))
                return True
    return False
