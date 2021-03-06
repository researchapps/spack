# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTensora(RPackage):
    """The package provides convenience functions for advance linear algebra
       with tensors and computation with datasets of tensors on a higher level
       abstraction."""

    homepage = "https://cloud.r-project.org/package=tensorA"
    url      = "https://cloud.r-project.org/src/contrib/tensorA_0.36.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tensorA"

    version('0.36.1', sha256='c7ffe12b99867675b5e9c9f31798f9521f14305c9d9f9485b171bcbd8697d09c')
    version('0.36', '01c0613491d9b46600bf403d7e3bdd80')

    depends_on('r@2.2.0:', type=('build', 'run'))
