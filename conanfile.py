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
        self.copy('*.dll', dst='bin', keep_path=True)
        self.copy('lib*',  dst='lib', keep_path=True)
        self.copy('*lib',  dst='lib', keep_path=True)
        self.copy('*.pc',  dst='lib/pkgconfig', keep_path=True)
        self.copy('*.1',   dst='share/man/man1', keep_path=True)
        self.copy('lz4',   dst='bin', keep_path=True)
        self.copy('*.h',   dst='include', keep_path=True)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
