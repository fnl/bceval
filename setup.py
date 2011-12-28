from distutils.core import setup

from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values(): 
    scheme['data'] = scheme['purelib']

setup(
    name='bc_evaluation',
    version='3.0.1',
    description='Official BioCreative evaluation script.',
    license='GNU GPL, latest version',
    author='Florian Leitner',
    author_email='fleitner@cnio.es',
    url='http://www.biocreative.org/resources/biocreative-ii5/evaluation-library/',
    packages=[
        'biocreative',
        'biocreative.evaluation',
        'biocreative.evaluation.calculation',
        'biocreative.evaluation.container',
        'biocreative.evaluation.controller',
        'biocreative.evaluation.file_io',
        'biocreative.evaluation.map_filter',
    ],
    package_dir={'biocreative.evaluation': 'biocreative/evaluation'},
    package_data={'biocreative.evaluation': ['configuration.ini']},
    scripts=['bc-evaluate']
)
