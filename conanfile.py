#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools


class Lz4Conan(ConanFile):
    name            = 'lz4'
    version         = '1.8.3'
    license         = 'MIT'
    author          = 'Matthew Russell <mrussell@neptec.com>'
    url             = 'NTC'
    description     = 'Extremely Fast Compression algorithm'
    requires        = ()
    options         = {'shared': [True, False]}
    default_options = 'shared=False'

    settings        = {
        'os':         ['Windows'],
        'build_type': ['Release'],
        'arch':       ['x86', 'x86_64']
    }

    def source(self):
        tools.get(
            url='https://github.com/lz4/lz4/releases/download/v1.8.3/lz4_v1_8_3_%s.zip'%('win64' if 'x86_64' == self.settings.arch else 'win32'),
            filename='lz4.zip',
            md5='0c6d61689d433956097c9ef543af5a60' if 'x86_64' == self.settings.arch else '03c6b676449f448a750186d1e048d8db'
        )

    def package(self):
        self.copy('*.exe', dst='bin',     keep_path=False)
        if self.options.shared:
            self.copy('*.dll', dst='bin',               keep_path=False)
            self.copy('*.lib', dst='lib', src='dll',    keep_path=False)
        else:
            self.copy('*.lib', dst='lib', src='static', keep_path=False)

        self.copy('*.h',   dst='include', keep_path=False)

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ['lz4']
            self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        else:
            self.cpp_info.libs = ['lz4_static']

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
