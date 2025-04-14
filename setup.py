from setuptools import setup

setup(
    name='te-clamSearch',
    version='0.1',
    packages=["clam", "clam.common"],
    description='TE Cleam AV Search & Drop Tool',
    author='Will Koester',
    author_email='wikoeste@cisco.com',
    url='https://github.com/wikoeste/talos-te-clamsearch.git',
    entry_points={
        'console_scripts':[
            'te-clamSearch=clam.main:main',
            ],
        },
)