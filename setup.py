import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='spookify',
    version='0.2.2',
    author='George Watson',
    author_email='george@georgewatson.me',
    description='Pun generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/georgewatson/spookify',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=[
        'jellyfish',
        'regex',
    ],
    include_package_data=True,
    zip_safe=False)
