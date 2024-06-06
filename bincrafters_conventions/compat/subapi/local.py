class CompatLocalAPI:

    def __init__(self, compat_api):
        self.compat_api = compat_api

    def compat_inspect_attribute(self, conanfile: str, attribute: str):
        """Return a single recipe attribute.
        Return None if the attribute does not exist 
        """

        value = None
        if self.compat_api.conan_version >= "2.0.0":
            import inspect as python_inspect

            conanfile_class = self.compat_api.ConanAPI.local.inspect(conanfile_path=conanfile, remotes=None, lockfile=None)

            for attr_name, attr_value in python_inspect.getmembers(conanfile_class):
                if attr_name == attribute:
                    value = attr_value
                    break

            print(f"higher than 2.0 value: {value}")
        else:
            value = self.compat_api.ConanAPI.inspect(path=conanfile, attributes=[attribute])[attribute]
            print(f"lower than 2.0 value: {value}")

        return value
