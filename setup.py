from setuptools import setup, find_packages
import sofaconventions.SOFAAPI


setup(
    name='sofaconventions',
    version=sofaconventions.SOFAAPI.getAPIVersion(),
    description='sofaconventions: python implementation of the SOFA Convention',
    author='Andres Perez-Lopez',
    author_email='andres.perez@upf.edu',
    url='https://andresperezlopez.github.io/sofaconventions/',
    packages=['sofaconventions'],
    long_description='sofaconventions: python implementation of the Spatially Oriented Format for Acoustics Convention',
    keywords='SOFA HRTF binaural Ambisonics',
    project_urls={
        'Project page': 'https://andresperezlopez.github.io/sofaconventions/',
        'Documentation': 'https://sofaconventions.readthedocs.io/',
        'Source': 'https://github.com/andresperezlopez/sofaconventions',
    },
    license='BSD-3-Clause',
    classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Development Status :: 3 - Alpha",
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
        ],
    # install_requires=[
    # ],
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
