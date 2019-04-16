import os
import re


def _get_docker_image_name(compiler: str, version):
    OWNER = 'conanio'

    version = str(version)
    image_version = version.replace(".", "")
    if compiler == "clang" and version == "7.0":
        image_version = '7'

    return "{}/{}{}".format(OWNER, compiler, image_version)


def _create_new_job(platform: dict, compiler: str, version, job: str, old_version, images_mapping: dict):
    old_version_str = "CONAN_{}_VERSIONS{}{}".format(compiler.upper(), platform["delimiter"], old_version)
    new_version_str = "CONAN_{}_VERSIONS{}{}".format(compiler.upper(), platform["delimiter"], version)
    job = job.replace(old_version_str, new_version_str)

    if compiler == "gcc" or compiler == "clang":
        old_docker_image_str = "CONAN_DOCKER_IMAGE={}".format(_get_docker_image_name(compiler, old_version))
        new_docker_image_str = "CONAN_DOCKER_IMAGE={}".format(_get_docker_image_name(compiler, version))
        job = job.replace(old_docker_image_str, new_docker_image_str)

    elif compiler == "apple_clang":
        old_image = images_mapping[old_version]
        new_image = images_mapping[version]
        old_image_str = "osx_image: xcode{}".format(old_image)
        new_image_str = "osx_image: xcode{}".format(new_image)
        job = job.replace(old_image_str, new_image_str)

    elif compiler == "visual":
        old_image = images_mapping[old_version]
        new_image = images_mapping[version]
        old_image_str = "APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio {}".format(old_image)
        new_image_str = "APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio {}".format(new_image)
        job = job.replace(old_image_str, new_image_str)

    return job


def update_add_new_compiler_versions(main, file, platform: dict, compiler_versions: dict, images_mapping: dict, compiler_deleting: dict):
    """ This update script updates CI jobs, adds new compilers, deleted obsolete ones

    :param file: CI file path
    :param platform: CI specific platform information
    :param compiler_versions: List of recommended new compiler versions
    :param images_mapping: Mapping of compiler version to specific CI runtime images
    :param compiler_deleting: Compiler versions which are getting deleted
    """

    platform_name = platform["name"]
    platform_jobs_beginning_keywords = platform["beginning_keywords"]
    platform_jobs_end_keyword = platform["end_keyword"]

    beginning_found_end = len(platform_jobs_beginning_keywords)
    beginning_found_threshold = beginning_found_end - 1
    beginning_found = -1  # -1, 0 (one of two starting criteria are found) or 1 (both criteria are found), 2 end

    latest_versions = {'a_unidentified': 0, 'gcc': 0, 'clang': 0, 'apple_clang': 0, 'visual': 0}
    versions_jobs = {'a_unidentified': {}, 'gcc': {}, 'clang': {}, 'apple_clang': {}, 'visual': {}}

    # Strings for file content
    new_content_beginning = ""
    compiler_jobs = ""
    new_content_end = "\n"

    manipulated_jobs = False
    current_compiler = ""
    current_compiler_version = 0

    tmp = ""
    compiler_found = False

    if not os.path.isfile(file):
        return False

    with open(file) as ifd:
        for line in ifd:
            # search for the start of the actual jobs
            if beginning_found != beginning_found_threshold:

                # Add this line to the new file
                if beginning_found == beginning_found_end:
                    new_content_end += line
                else:
                    new_content_beginning += line

                # Search for the first keyword
                if line.strip() == platform_jobs_beginning_keywords[0]:
                    beginning_found = 0
                    continue

                # Skip empty lines and comments between the first and last keyword
                if line.strip() is "" or line.strip()[0] == "#":
                    continue

                # Search for all the other keywords
                if beginning_found >= 0 and beginning_found < beginning_found_end:
                    if line.strip() == platform_jobs_beginning_keywords[beginning_found+1]:
                        beginning_found += 1
                        continue

                # The keywords need to be in the right order, if not something is wrong
                if beginning_found != beginning_found_end:
                    beginning_found = -1

            else:
                # look for end of jobs list
                if line.strip() == platform_jobs_end_keyword:
                    # Add this line to the new file
                    new_content_end += line
                    beginning_found = beginning_found_end
                    continue

                # Skip empty lines and comments
                if line.strip() is "" or line.strip()[0] == "#":
                    continue

                # Are we entering a new job?
                if line.strip()[0] == "-":
                    # There are jobs which compiler we can't identify, make sure we don't delete them
                    # This applies for e.g. mingw jobs on AppVeyor
                    if tmp != "" and compiler_found == False:
                        versions_jobs["a_unidentified"]["v1"] = \
                            versions_jobs["a_unidentified"].get("v1", "") + tmp

                    current_compiler = ""
                    current_compiler_version = 0
                    compiler_found = False
                    tmp = line

                # What compiler are we currently looking at?
                for compiler_name, _ in compiler_versions.items():
                    regex_compiler = re.compile("CONAN_{}".format(compiler_name.upper())
                                                + "_VERSIONS{}" .format(platform["delimiter"])
                                                + r'([^\s]+)')
                    if regex_compiler.search(line):
                        current_compiler = compiler_name
                        current_compiler_version = regex_compiler.search(line).group(1)
                        compiler_found = True
                        versions_jobs[current_compiler]['v'+current_compiler_version] = versions_jobs[current_compiler].get("v"+current_compiler_version, "") + tmp
                        break

                if compiler_found:
                    versions_jobs[current_compiler]['v'+current_compiler_version] = versions_jobs[current_compiler].get("v"+current_compiler_version, "") + line

                    # Did we found a newer compiler version?
                    if float(latest_versions[current_compiler]) < float(current_compiler_version):
                        latest_versions[current_compiler] = current_compiler_version

                elif tmp != line:
                    tmp += line

    # Add new compiler versions
    # Loop over recommended new compiler versions
    for compiler, versions in compiler_versions.items():
        # Version 0 means that there are no jobs for this compiler existing
        # So we don't want to add new jobs for this compiler either
        # Not all packages support all compiler/platforms
        if latest_versions[compiler] == 0:
            continue

        for version in versions:
            # We are only adding compiler versions which are newer than the newest currently already existing
            # Meaning: If someone is removing older compiler versions we aren't going to re-add them
            if float(latest_versions[compiler]) < float(version):
                manipulated_jobs = True
                update_message = "{}: Add job(s) for new compiler version {} {}".format(platform_name, compiler, version)
                main.output_result_update(title=update_message)

                latest_version = latest_versions[compiler]
                base_job = versions_jobs[compiler]["v"+latest_versions[compiler]]
                new_job = _create_new_job(platform, compiler, version, base_job, latest_version, images_mapping)
                versions_jobs[compiler]['v' + version] = new_job

    # Now use the compiler jobs information and transform them back into a writeable string
    for compiler, _ in versions_jobs.items():
        if compiler != "a_unidentified":
            for key in sorted(versions_jobs[compiler].keys(), key=lambda s: float(s[1:])):
                # Check if we do have old compiler version which we want to delete
                if key[1:] in compiler_deleting[compiler]:
                    manipulated_jobs = True
                    update_message = "{}: Delete job(s) for old compiler version {} {}".format(platform_name, compiler, key[1:])
                    main.output_result_update(title=update_message)
                else:
                    compiler_jobs += versions_jobs[compiler][key]
        else:
            # For jobs were we didn't identify the compiler we just leave the jobs unmodified
            compiler_jobs += versions_jobs[compiler].get("v1", "")

    # With all gained information re-write the Travis file now if we actually found missing compiler versions
    if manipulated_jobs:
        with open(file, 'w') as fd:
            fd.write(new_content_beginning + compiler_jobs + new_content_end)
