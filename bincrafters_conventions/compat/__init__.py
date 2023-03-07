from bincrafters_conventions.compat.subapi.graph import CompatGraphAPI

# Naming Convention:
#   Class Names for sub APIs have to start with Compat
#   Attribute names for sub APIs should be as similar to the v2 Conan API as possible
#   Function names in the APIs should either
#       start with compat_ if they do not exist with the same behaviour in the v2 Conan API
#       or be named exactly as in the v2 Conan API if the behaviour is identical

class CompatConanAPI():
    def __init__(self):
        try:
            from conan import conan_version as client_version
            from conan.api.conan_api import ConanAPI as conan_api
        except:
            from conans import __version__ as client_version
            from conans.client import conan_api
        
        from conan.tools.scm import Version

        # For sub APIs consumers
        self._Version = Version

        # Public 
        self.conan_version = self._Version(client_version)
        self.ConanAPI = conan_api
        self.graph = CompatGraphAPI(self)
