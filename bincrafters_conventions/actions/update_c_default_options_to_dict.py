import re
from conans.errors import ConanException
from conans.client import conan_api


def _get_default_options(file):
    conan_instance, _, _ = conan_api.Conan.factory()
    try:
        result = conan_instance.inspect(path=file, attributes=['default_options'])['default_options']
        new_result = {}
        # Tuple uses old combination: "value=key"
        if isinstance(result, tuple):
            for item in result:
                # extract key,value from string
                match = re.match(r'(.*)=(.*)', item)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                    # to boolean
                    if value == 'True' or value == 'False':
                        value = value == 'True'
                    new_result[key] = value
            return new_result
        # if we only have one option it is a string
        if isinstance(result, str):
            item = result.split("=")
            new_result[item[0]] = item[1]
            return new_result
        return None
    except ConanException:
        return None


def update_c_default_options_to_dict(main, file):
    attribute = 'default_options'
    default_options = _get_default_options(file)
    if default_options is None:
        return False
    with open(file) as ifd:
        content = ifd.readlines()
        with open(file, 'w') as ofd:
            found_default_options = False
            updated = False
            for line in content:
                if not found_default_options:
                    # searching for default options
                    if attribute in line:
                        found_default_options = True
                        line = '    {} = {}\n'.format(attribute, default_options)
                    # searching for multiline default options
                elif found_default_options and not updated:
                    if ')' in line or re.search(r'".*=', line):
                        continue
                    else:
                        updated = True
                ofd.write('{}'.format(line))
            # ofd.write('\n')

    if updated:
        main.output_result_update(title="Convert default_options to a dictionary")
        return True
    else:
        return False
