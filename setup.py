from setuptools import setup, find_packages
try:
    import md5  # fix for "No module named _md5" error
except ImportError:
    # python 3 moved md5
    from hashlib import md5

with open("README.rst") as f:
    long_description = f.read()


setup(name='expiringdict',
      version='0.0.2',
      description="Dictionary with auto-expiring values for caching purposes. Based on Anton Efimenko's expiringdict.",
      long_description=long_description,
      author='Ben Auffarth',
      author_email='auffarth@gmail.com',
      url='https://github.com/benman1/ExpiryCache.git',
      license='Apache 2',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True,
      extras_require={'test': ['nose', 'mock', 'coverage']})
