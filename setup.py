#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'requests>=2.8.1',
    'elasticsearch>=1.5.0',
    'cython>=0.22',
    'thriftpy>=0.3.1',
    'thriftpywrap',
    'xylose>=1.16.5',
    'pyramid>=1.5.7',
    'pyramid_chameleon',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'waitress',
    ]

test_requires = []

setup(
    name="access",
    version='0.6.4',
    description="A SciELO RPC server and API to retrieve access statistics from the SciELO Network ",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD 2-clause",
    url="http://docs.scielo.org",
    keywords='scielo statistics',
    packages=['access'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: Services",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    dependency_links=[
        "git+https://github.com/scieloorg/thriftpy-wrap@0.1.1#egg=thriftpywrap"
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=["nose>=1.0", "coverage"],
    tests_require=test_requires,
    install_requires=install_requires,
    test_suite="nose.collector",
    entry_points="""\
    [paste.app_factory]
    main = access:main
    [console_scripts]
    accessstats_thriftserver = access.thrift.server:main
    """,
)