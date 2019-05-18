from setuptools import find_packages, setup

import pysofaconventions.SOFAAPI

setup(
    name='pysofaconventions',
    version=pysofaconventions.SOFAAPI.getAPIVersion(),
    description='pysofaconventions: python implementation of the SOFA Convention',
    author='Andres Perez-Lopez',
    author_email='andres.perez@upf.edu',
    url='https://andresperezlopez.github.io/pysofaconventions/',
    packages=find_packages(),
    long_description='pysofaconventions: python implementation of the Spatially Oriented Format for Acoustics Convention',
    keywords='SOFA HRTF binaural Ambisonics',
    project_urls={
        'Project page': 'https://andresperezlopez.github.io/pysofaconventions/',
        'Documentation': 'https://pysofaconventions.readthedocs.io/',
        'Source': 'https://github.com/andresperezlopez/pysofaconventions',
    },
    license='BSD-3-Clause',
    classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Topic :: Multimedia :: Sound/Audio :: Analysis",
            "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
    install_requires=[
        'netCDF4'
    ],
    extras_require={
        'docs': [
                'sphinx==1.2.3',  # autodoc was broken in 1.3.1
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
        # 'tests': ['backports.tempfile', 'pysoundfile']
    }
)
