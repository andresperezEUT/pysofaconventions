from setuptools import setup, find_packages
import pysofa.SOFAAPI


setup(
    name='pysofa',
    version=pysofa.SOFAAPI.getAPIVersion(),
    description='pysofa: python implementation of the SOFA conventions',
    author='Andres Perez-Lopez',
    author_email='andres.perez@upf.edu',
    url='https://andresperezlopez.github.io/pysofa/',
    packages=['pysofa'],
    long_description='pysofa: python implementation of the SOFA conventions',
    keywords='SOFA HRTF binaural Ambisonics',
    project_urls={
        'Project page': 'https://andresperezlopez.github.io/pysofa/',
        'Documentation': 'https://pysofa.readthedocs.io/',
        'Source': 'https://github.com/andresperezlopez/pysofa',
    },
    license='GNU GPLv3.0',
    classifiers=[
            "Development Status :: 4 - Beta"
            "License :: OSI Approved :: GNU GPLv3.0",
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
