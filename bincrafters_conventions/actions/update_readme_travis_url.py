def update_readme_travis_url(main, file):
    """ Update Travis CI URL
    """
    if main.replace_in_file(file, "https://travis-ci.org/bincrafters", "https://travis-ci.com/bincrafters"):
        main.output_result_update(title="README: Update Travis URL from .org to .com")
        return True
    return False
