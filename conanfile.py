import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class Lz4Conan(ConanFile):
    name            = 'lz4'
    version         = '1.8.3'
    license         = '<Put the package license here>'
    author          = '<Put your name here> <And your email here>'
    url             = 'NTC'
    description     = 'Extremely Fast Compression algorithm'
    settings        = 'os', 'compiler', 'build_type', 'arch'
    requires        = 'helpers/[>=0.3]@ntc/stable'
    options         = {
        # This builds both the static and shared libs each time, so this option
        # is really only used to decorate the package in Windows with the
        # proper RUNTIME variable
        'shared': [True, False],

        # Option only used to decorate the package
        'msvc':   [12, 15]
    }
    default_options = 'shared=True', 'msvc=12'

    def config_options(self):
        if not tools.os_info.is_windows:
            self.options.remove('shared')

    def source(self):
        g = tools.Git(self.name)
        g.clone('https://github.com/lz4/lz4.git', branch='v%s'%self.version)

    def build(self):
        with tools.chdir(self.name):
            # There's no configure, only a custom Makefile with an install
            # target which conan won't let me inject variables in to, and even
            # when I do, because it's built with mingw the paths are wrong.
            # So, build, then just manually package.
            at = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            at.make()

    def package(self):
        self.copy('*.dll', dst='bin')
        self.copy('lib*',  dst='lib')
        self.copy('*lib',  dst='lib')
        self.copy('*.pc',  dst='lib/pkgconfig')
        self.copy('*.1',   dst='share/man/man1')
        self.copy('lz4',   dst='bin')
        self.copy('*.h',   dst='include/lz4')

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if tools.os_info.is_windows:
            self.env_info.path.append(os.path.join(self.package_folder, 'bin'))

        # Populate the pkg-config environment variables
        with tools.pythonpath(self):
            from platform_helpers import adjustPath, appendPkgConfigPath
            self.env_info.PKG_CONFIG_LZ4_PREFIX = adjustPath(self.package_folder)
            appendPkgConfigPath(adjustPath(os.path.join(self.package_folder, 'lib', 'pkgconfig')), self.env_info)

    def package_id(self):
        # On windows, we cross compile this with mingw.. But because it's
        # compatible with MSVC, set it's hash to reflect that.
        # Maybe use tools.cross_building(self.settings)
        if 'gcc' == self.settings.compiler and tools.os_info.is_windows:
            self.info.settings.compiler = 'Visual Studio'
            self.info.settings.compiler.version = int(str(self.options.msvc))

            runtime = 'MD' if self.options.shared else 'MT'
            if self.settings.build_type == 'Debug':
                runtime += 'd'
            self.info.settings.compiler.runtime = runtime

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
