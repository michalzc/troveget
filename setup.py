from setuptools import setup

setup(
  name="TroveGet",
  version="0.1",
  packages=["troveget"],
  install_requires=[
    'requests==2.23.0',
    'beautifulsoup4==4.9.0'
  ],
  test_suit='nose.collector',
  tests_require=[
    'nose'
  ],
  entry_points='''
    [console_scripts]
    trove-get=troveget:get
  '''
)
