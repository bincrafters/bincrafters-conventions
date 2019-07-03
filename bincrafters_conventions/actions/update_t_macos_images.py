def update_t_macos_images(main, file, xcode_versions_to_check):
    """ Sometimes Travis is publishing new CI images with new XCode versions
        but they still have the same Clang version
        in this case we do NOT need to add new compiler versions and therefore jobs
        but we need to update the existing jobs
    """

    updated = False

    for xcode_update in xcode_versions_to_check:
        old_image_version = xcode_update[0]
        new_image_version = xcode_update[1]

        current_image_string = "osx_image: xcode{}\n".format(old_image_version)
        new_image_string = "osx_image: xcode{}\n".format(new_image_version)

        if main.file_contains(file, current_image_string):
            if (main.replace_in_file(file, current_image_string, new_image_string)):
                main.output_result_update(title="Travis: Update macOS CI image from {} to {}".format(old_image_version, new_image_version))
                updated = True

    if updated:
        return True

    return False
