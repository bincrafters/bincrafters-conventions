import os


def update_gha(main, file, gha_workflow_version):
    """ This update script updates the GHA script

    :param file: CI file path
    :param gha_workflow_version: Current version (int) of workflow file
    """

    file_content = ""
    tag = "# bincrafters-conventions:gha-workflow-version:"
    script_start_found = False

    with open(file) as ifd:
        for line in ifd:
            if script_start_found is False:
                if line.strip().startswith(tag):
                    workflowVersion = line.strip().replace(tag, "")
                    if workflowVersion >= gha_workflow_version:
                        return False
                    else:
                        script_start_found = True
                else:
                    file_content += line

    basepath = os.path.dirname(__file__)
    with open(os.path.join(basepath, "update_gha.yml")) as fp:
        file_content += fp.read()

    with open(file, 'w') as fd:
        fd.write(file_content)

    update_message = "GitHub Actions: Update CI script"
    main.output_result_update(title=update_message)

    return True




