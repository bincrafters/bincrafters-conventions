import re


def _leading_line_spaces(line):
    return len(line) - len(line.lstrip())


def _create_new_job(platform: dict, compiler: str, version, job: str, old_version, images_mapping: dict):
    old_version_str = "CONAN_{}_VERSIONS{}{}".format(compiler.upper(), platform["delimiter"], old_version)
    new_version_str = "CONAN_{}_VERSIONS{}{}".format(compiler.upper(), platform["delimiter"], version)
    job = job.replace(old_version_str, new_version_str)

    if compiler == "visual":
        old_image = images_mapping[old_version]
        new_image = images_mapping[version]
        old_image_str = "APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio {}".format(old_image)
        new_image_str = "APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio {}".format(new_image)
        job = job.replace(old_image_str, new_image_str)

    return job


def update_add_new_compiler_versions(main, file, platform: dict, compiler_versions: dict, images_mapping: dict,
                                     compiler_deleting: dict):
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
    # Indication that a new job in the matrix is beginning, i.e. "-" (a hyphen)
    platform_job_beginning_indication = platform["job_beginning_indication"]
    # Some platforms like AZP don't use a symbol to indicate new jobs, we need to interprete the indentation correctly
    platform_job_beginning_indication_use_spaces = platform["job_beginning_indication_use_spaces"]
    platform_job_beginning_indication_spaces_amount = -1

    beginning_found_end = len(platform_jobs_beginning_keywords)
    beginning_found_threshold = beginning_found_end - 1
    beginning_found = -1

    latest_versions = {'a_unidentified': 0, 'visual': 0}
    versions_jobs = {'a_unidentified': {}, 'visual': {}}

    # Strings for file content
    new_content_beginning = ""
    compiler_jobs = ""
    new_content_end = "\n"

    manipulated_jobs = False
    current_compiler = ""
    current_compiler_version = 0

    tmp = ""
    compiler_found = False

    # Markers to categorize a single CI job
    # ARCH for installer, CONAN_ARCHS for libraries
    arch_marker32 = "CONAN_ARCHS{}x86".format(platform["delimiter"])
    arch_marker32_alt1 = "CONAN_ARCHS{}'x86'".format(platform["delimiter"])
    arch_marker32_alt2 = 'CONAN_ARCHS{}"x86"'.format(platform["delimiter"])
    arch_marker32_alt3 = "CONAN_ARCHS{}x86".format(platform["delimiter"])
    arch_marker32_alt4 = 'ARCH{}"x86"'.format(platform["delimiter"])
    arch_marker32_alt5 = "ARCH{}'x86'".format(platform["delimiter"])
    arch_marker32_alt6 = "ARCH{}x86".format(platform["delimiter"])
    arch_marker64 = "CONAN_ARCHS{}x86_64".format(platform["delimiter"])
    arch_marker64_alt1 = "CONAN_ARCHS{}'x86_64'".format(platform["delimiter"])
    arch_marker64_alt2 = 'CONAN_ARCHS{}"x86_64"'.format(platform["delimiter"])
    arch_marker64_alt3 = "CONAN_ARCHS{}x86_64".format(platform["delimiter"])
    arch_marker64_alt4 = 'ARCH{}"x86_64"'.format(platform["delimiter"])
    arch_marker64_alt5 = "ARCH{}'x86_64'".format(platform["delimiter"])
    arch_marker64_alt6 = "ARCH{}x86_64".format(platform["delimiter"])

    mingw_marker = "MINGW_CONFIGURATIONS"

    # Tags, which can be added to individual config files
    convention_tag = "bincrafters-conventions:"
    convention_tag_preserve_job = "preserve-build-job"
    convention_tag_no_new_compiler_versions = "no-new-compiler-versions"

    remove_current_job = False
    preserve_current_job = False
    tag_no_new_compiler_versions = False

    def _save_tmp_to_job(tmp_string):
        if tmp_string != "":
            if preserve_current_job or remove_current_job is False:
                # There are jobs which compiler we can't identify, make sure we don't delete them
                # This applies for e.g. mingw jobs on AppVeyor
                if compiler_found is False:
                    versions_jobs["a_unidentified"]["v1"] = \
                        versions_jobs["a_unidentified"].get("v1", "") + tmp_string
                else:
                    versions_jobs[current_compiler]['v' + current_compiler_version] = \
                        versions_jobs[current_compiler].get("v" + current_compiler_version, "") + tmp_string
            else:
                if current_compiler_version == 0:
                    main.output_result_update(title="{}: Removed obsolete MinGW build job".format(platform_name))
                else:
                    main.output_result_update(title="{}: Removed obsolete 32-bit build job for {} {}"
                                          .format(platform_name, current_compiler, current_compiler_version))
                nonlocal manipulated_jobs
                manipulated_jobs = True

    with open(file) as ifd:
        for line in ifd:
            if "{}{}".format(convention_tag, convention_tag_no_new_compiler_versions) in line:
                tag_no_new_compiler_versions = True

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
                if line.strip() == "" or line.strip()[0] == "#":
                    continue

                # Search for all the other keywords
                if beginning_found >= 0 and beginning_found < beginning_found_end:
                    if line.strip() == platform_jobs_beginning_keywords[beginning_found + 1]:
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
                if line.strip() == "" or line.strip()[0] == "#":
                    continue

                if platform_job_beginning_indication_use_spaces \
                        and platform_job_beginning_indication_spaces_amount == -1:
                    # This is a platform which uses indentation to signalizes the beginning of a new build job
                    # On the very first job we need to figure out the amount of spaces so we can detect the beginning of
                    # all following build jobs. This is the case on i.e. AZP
                    platform_job_beginning_indication_spaces_amount = _leading_line_spaces(line)

                # Are we entering a new job?
                if (platform_job_beginning_indication_use_spaces
                    and platform_job_beginning_indication_spaces_amount == _leading_line_spaces(line)) \
                        or (platform_job_beginning_indication_use_spaces is False
                            and line.strip()[0] == platform_job_beginning_indication):
                    _save_tmp_to_job(tmp)

                    tmp = ""
                    remove_current_job = False
                    preserve_current_job = False
                    current_compiler = ""
                    current_compiler_version = 0
                    compiler_found = False

                if (arch_marker64 not in line and arch_marker32 in line) \
                        or (arch_marker64_alt1 not in line and arch_marker32_alt1 in line) \
                        or (arch_marker64_alt2 not in line and arch_marker32_alt2 in line) \
                        or (arch_marker64_alt3 not in line and arch_marker32_alt3 in line) \
                        or (arch_marker64_alt4 not in line and arch_marker32_alt4 in line) \
                        or (arch_marker64_alt5 not in line and arch_marker32_alt5 in line) \
                        or (arch_marker64_alt6 not in line and arch_marker32_alt6 in line) \
                        or mingw_marker in line:
                    remove_current_job = True

                if "{}{}".format(convention_tag, convention_tag_preserve_job) in line:
                    preserve_current_job = True

                # What compiler are we currently looking at?
                for compiler_name, _ in compiler_versions.items():
                    regex_compiler = re.compile("CONAN_{}".format(compiler_name.upper())
                                                + "_VERSIONS{}".format(platform["delimiter"])
                                                + r'([^\s]+)')
                    if regex_compiler.search(line):
                        current_compiler = compiler_name
                        current_compiler_version = regex_compiler.search(line).group(1)
                        compiler_found = True

                        # Did we found a newer compiler version?
                        if float(latest_versions[current_compiler]) < float(current_compiler_version):
                            latest_versions[current_compiler] = current_compiler_version

                        break

                tmp += line

    # Add very last job
    _save_tmp_to_job(tmp)

    # Add new compiler versions
    # Loop over recommended new compiler versions
    if tag_no_new_compiler_versions is False:
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
                    update_message = "{}: Add job(s) for new compiler version {} {}".format(platform_name, compiler,
                                                                                            version)
                    main.output_result_update(title=update_message)

                    latest_version = latest_versions[compiler]
                    base_job = versions_jobs[compiler]["v" + latest_versions[compiler]]
                    new_job = _create_new_job(platform, compiler, version, base_job, latest_version, images_mapping)
                    versions_jobs[compiler]['v' + version] = new_job

    # Now use the compiler jobs information and transform them back into a writeable string
    for compiler, _ in versions_jobs.items():
        if compiler != "a_unidentified":
            for key in sorted(versions_jobs[compiler].keys(), key=lambda s: float(s[1:])):
                # Check if we do have old compiler version which we want to delete
                if key[1:] in compiler_deleting[compiler]:
                    manipulated_jobs = True
                    update_message = "{}: Delete job(s) for old compiler version {} {}".format(platform_name, compiler,
                                                                                               key[1:])
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

    return manipulated_jobs
