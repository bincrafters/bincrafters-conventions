class CompatGraphAPI:

    def __init__(self, compat_api):
        self.compat_api = compat_api

    def compat_inspect_attribute(self, conanfile: str, attribute: str):
        """Return a single recipe attribute.
        Return None if the attribute does not exist 
        """

        value = None
        if self.compat_api.conan_version >= "2.0.0":
            
            conanfile_class = self.compat_api.ConanAPI.graph.load_conanfile_class(path=conanfile)
            print(conanfile_class)
            print(f"higher than 2.0 value: {conanfile_class}")
        else:
            conan_instance, _, _ = self.compat_api.ConanAPI.Conan.factory()
            value = conan_instance.inspect(path=conanfile, attributes=[attribute])[attribute]
            print(f"lower than 2.0 value: {value}")

        return value
