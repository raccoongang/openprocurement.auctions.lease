from setuptools import setup, find_packages
import os

version = '1.1.1-sale'

entry_points = {
    'openprocurement.auctions.core.plugins': [
        'auctions.lease = openprocurement.auctions.lease.includeme:includeme_lease'
    ],
    'openprocurement.api.migrations': [
        'auctions = openprocurement.auctions.lease.migration:migrate_data'
    ],
    'openprocurement.tests': [
        'auctions.lease = openprocurement.auctions.lease.tests.main:suite'
    ]
}

requires = [
    'setuptools',
    'openprocurement.api',
    'openprocurement.auctions.core',
]

docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]

setup(name='openprocurement.auctions.lease',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/raccoongang/openprocurement.auctions.lease',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.auctions'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'docs': docs_requires},
      install_requires=requires,
      entry_points=entry_points,
      )
