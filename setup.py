#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'aiohttp[speedups]',
    'aiocache[redis]',
    # 'pyyaml',
    # 'pytz',
    # 'requests',
    'uri',
    'Click>=7.0',
    'aioredis<2.0.0',
]

test_requirements = [ ]

setup(
    author="Mauro Amico",
    author_email='mauro.amico@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'rss_asyncio_proxy=rss_asyncio_proxy.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='rss_asyncio_proxy',
    name='rss_asyncio_proxy',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mamico/rss_asyncio_proxy',
    version='0.1.0',
    zip_safe=False,
)
