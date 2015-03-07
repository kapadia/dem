
from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='toDEM',
      version='0.0.1',
      description=u"GeoJSON to DEM",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Amit Kapadia",
      author_email='akapad@gmail.com',
      url='https://github.com/kapadia/dem',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'rasterio',
          'numpy',
          'scipy',
          'pyproj',
          'affine'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      dem=dem.scripts.cli:cli
      """
      )
