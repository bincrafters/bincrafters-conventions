import os


def update_gha(main, file):
    """ This update script updates the GHA script

    :param file: CI file path
    """

    gha_workflow_version = None
    file_content = ""
    tag = "# bincrafters-conventions:gha-workflow-version:"

    with open(os.path.join(os.path.dirname(__file__), "update_gha.yml"), encoding="utf-8") as ifd:
        for line in ifd:
            if line.strip().startswith(tag):
                gha_workflow_version = line.strip().replace(tag, "")
                break

    with open(file, encoding="utf-8") as ifd:
        for line in ifd:
            if line.strip().startswith(tag):
                workflow_version = line.strip().replace(tag, "")
                if int(workflow_version) >= int(gha_workflow_version):
                    return False
                else:
                    break
            else:
                file_content += line

    if int(workflow_version) < 10:
        file_content += "on: [push, pull_request]\n\n"

    basepath = os.path.dirname(__file__)
    with open(os.path.join(basepath, "update_gha.yml"), encoding="utf-8") as fp:
        file_content += fp.read()

    with open(file, 'w', encoding="utf-8") as fd:
        fd.write(file_content)

    update_message = "GitHub Actions: Update CI script to version {}".format(gha_workflow_version)
    main.output_result_update(title=update_message)

    return True




