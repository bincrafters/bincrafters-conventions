import os
import re


def _get_docker_image_name(compiler: str, version):
    OWNER = 'conanio'

    version = str(version)
    image_version = version.replace(".", "")
    if compiler == "clang" and version == "7.0":
        image_version = '7'

    return "{}/{}{}".format(OWNER, compiler, image_version)


def _create_new_job(compiler: str, version, job: str, old_version, macos_images_mapping: dict):
    old_version_str = "CONAN_{}_VERSIONS={}".format(compiler.upper(), old_version)
    new_version_str = "CONAN_{}_VERSIONS={}".format(compiler.upper(), version)
    job = job.replace(old_version_str, new_version_str)

    if compiler == "gcc" or compiler == "clang":
        old_docker_image_str = "CONAN_DOCKER_IMAGE={}".format(_get_docker_image_name(compiler, old_version))
        new_docker_image_str = "CONAN_DOCKER_IMAGE={}".format(_get_docker_image_name(compiler, version))
        job = job.replace(old_docker_image_str, new_docker_image_str)

    elif compiler == "apple_clang":
        old_image = macos_images_mapping[old_version]
        new_image = macos_images_mapping[version]
        old_image_str = "osx_image: xcode{}".format(old_image)
        new_image_str = "osx_image: xcode{}".format(new_image)
        job = job.replace(old_image_str, new_image_str)

    return job


def update_t_add_new_compiler_versions(main, file, travis_compiler_versions: dict, macos_images_mapping: dict):
    """ This update script adds new compiler versions to the Travis jobs

    :param file: Travis file path
    :param travis_compiler_version: List of recommended new compiler versions
    :param travis_macos_images_compiler_mapping: Mapping of apple_clang version to specific Travis images
    """

    beginning_found = -1  # -1, 0 (one of two starting criteria are found) or 1 (both criteria are found), 2 end
    latest_versions = {'gcc': 0, 'clang': 0, 'apple_clang': 0}
    versions_jobs = {'gcc': {}, 'clang': {}, 'apple_clang': {}}

    regex_gcc = re.compile(r'CONAN_GCC_VERSIONS=([^\s]+)')
    regex_clang = re.compile(r'CONAN_CLANG_VERSIONS=([^\s]+)')
    regex_apple_clang = re.compile(r'CONAN_APPLE_CLANG_VERSIONS=([^\s]+)')

    new_content_beginning = ""
    compiler_jobs = ""
    new_content_end = "\n"

    added_new_jobs = False
    current_compiler = ""
    current_compiler_version = 0

    tmp = ""
    compiler_found = False

    if not os.path.isfile(file):
        return False

    with open(file) as ifd:
        for line in ifd:
            # search for the start of the actual jobs
            if beginning_found != 1:

                # Add this line to the new file
                if beginning_found == 2:
                    new_content_end += line
                else:
                    new_content_beginning += line

                if line.strip() == "matrix:":
                    beginning_found = 0

                    continue
                if line.strip() == "include:" and beginning_found == 0:
                    beginning_found = 1
                    continue

                # The include: keywords needs to follow directly the matrix: keyword, if not something is wrong
                if beginning_found != 2:
                    beginning_found = -1

            else:
                # look for end of jobs list
                if line.strip() == "install:":
                    # Add this line to the new file
                    new_content_end += line
                    beginning_found = 2
                    continue

                # Skip empty lines
                if line.strip() is "":
                    continue

                # Are we entering a new job?
                if line.strip()[0] == "-":
                    current_compiler = ""
                    current_compiler_version = 0
                    compiler_found = False
                    tmp = line

                # What compiler are we currently looking at?
                if regex_gcc.search(line):
                    current_compiler = "gcc"
                    current_compiler_version = regex_gcc.search(line).group(1)
                    compiler_found = True
                    versions_jobs[current_compiler]['v'+current_compiler_version] = versions_jobs[current_compiler].get("v"+current_compiler_version, "") + tmp
                elif regex_clang.search(line):
                    current_compiler = "clang"
                    current_compiler_version = regex_clang.search(line).group(1)
                    compiler_found = True
                    versions_jobs[current_compiler]['v'+current_compiler_version] = versions_jobs[current_compiler].get("v"+current_compiler_version, "") + tmp
                elif regex_apple_clang.search(line):
                    current_compiler = "apple_clang"
                    current_compiler_version = regex_apple_clang.search(line).group(1)
                    compiler_found = True
                    versions_jobs[current_compiler]['v'+current_compiler_version] = versions_jobs[current_compiler].get("v"+current_compiler_version, "") + tmp

                if compiler_found:
                    versions_jobs[current_compiler]['v'+current_compiler_version] = versions_jobs[current_compiler].get("v"+current_compiler_version, "") + line

                    # Did we found a newer compiler version?
                    if float(latest_versions[current_compiler]) < float(current_compiler_version):
                        latest_versions[current_compiler] = current_compiler_version

                elif tmp != line:
                    tmp += line

    # Add new compiler versions
    # Loop over recommended new compiler versions
    for compiler, versions in travis_compiler_versions.items():
        # Version 0 means that there are no jobs for this compiler existing
        # So we don't want to add new jobs for this compiler either
        # Not all packages support all compiler/platforms
        if latest_versions[compiler] == 0:
            continue

        for version in versions:
            # We are only adding compiler versions which are newer than the newest currently already existing
            # Meaning: If someone is removing older compiler versions we aren't going to re-add them
            if float(latest_versions[compiler]) < float(version):
                added_new_jobs = True
                update_message = "Travis: Add job(s) for new compiler version {} {}".format(compiler, version)
                main.output_result_update(title=update_message)

                latest_version = latest_versions[compiler]
                base_job = versions_jobs[compiler]["v"+latest_versions[compiler]]
                new_job = _create_new_job(compiler, version, base_job, latest_version, macos_images_mapping)
                versions_jobs[compiler]['v' + version] = new_job

    # Now use the compiler jobs information and transform them back into a writeable string
    for compiler in ["gcc", "clang", "apple_clang"]:
        for key in sorted(versions_jobs[compiler].keys(), key=lambda s: float(s[1:])):
            compiler_jobs += versions_jobs[compiler][key]

    # With all gained information re-write the Travis file now if we actually found missing compiler versions
    if added_new_jobs:
        with open(file, 'w') as fd:
            fd.write(new_content_beginning + compiler_jobs + new_content_end)
