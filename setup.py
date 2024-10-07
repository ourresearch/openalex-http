from setuptools import setup, find_packages

setup(
    name='openalex-http',
    version='0.1',  # You can set your own version here.
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    package_data={
        'openalex_http.legacy': ['data/*']
    },
    include_package_data=True,
    url='https://github.com/ourresearch/openalex-http',
    license='',
    author='',
    author_email='',
    description=''
)
