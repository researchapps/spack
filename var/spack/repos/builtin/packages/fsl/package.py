# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.environment import EnvironmentModifications
import os


class Fsl(Package):
    """FSL is a comprehensive library of analysis tools for FMRI, MRI and DTI
       brain imaging data.

       Note: A manual download is required for FSL.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://fsl.fmrib.ox.ac.uk"
    url      = "file://{0}/fsl-5.0.10-sources.tar.gz".format(os.getcwd())

    version('5.0.10', '64823172a08aad679833240ba64c8e30')

    depends_on('python', type=('build', 'run'))
    depends_on('expat')
    depends_on('libx11')
    depends_on('glu')
    depends_on('zlib')
    depends_on('libpng')
    depends_on('boost')
    depends_on('sqlite')

    conflicts('%gcc@6:', when='@5.0.10')

    def patch(self):
        # Uncomment lines in source file to allow building from source
        with working_dir(join_path(self.stage.source_path, 'etc', 'fslconf')):
            sourced = FileFilter('fsl.sh')
            sourced.filter('#FSLCONFDIR', 'FSLCONFDIR')
            sourced.filter('#FSLMACHTYPE', 'FSLMACHTYPE')
        # Fix error in build script
        buildscript = FileFilter('build')
        buildscript.filter('mist-clean', 'mist')

    def install(self, spec, prefix):
        build = Executable('./build')
        build()

        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        if not self.stage.source_path:
            self.stage.fetch()
            self.stage.expand_archive()

        spack_env.set('FSLDIR', self.stage.source_path)

        # Here, run-time environment variables are being set manually.
        # Normally these would be added to the modulefile at build-time
        # by sourcing fsl.sh, but incorrect paths were being set, pointing to
        # the staging directory rather than the install directory.
        run_env.set('FSLDIR', self.prefix)
        run_env.set('FSLOUTPUTTYPE', 'NIFTI_GZ')
        run_env.set('FSLMULTIFILEQUIT', 'TRUE')
        run_env.set('FSLTCLSH', self.prefix.bin.fsltclsh)
        run_env.set('FSLWISH', self.prefix.bin.fslwish)
        run_env.set('FSLLOCKDIR', '')
        run_env.set('FSLMACHINELIST', '')
        run_env.set('FSLREMOTECALL', '')
        run_env.set('FSLGECUDAQ', 'cuda.q')

        run_env.prepend_path('PATH', self.prefix)

        # Below is for sourcing purposes during building
        fslsetup = join_path(self.stage.source_path, 'etc', 'fslconf',
                             'fsl.sh')

        if os.path.isfile(fslsetup):
            spack_env.extend(EnvironmentModifications.from_sourcing_file(
                             fslsetup))
