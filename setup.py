from setuptools import setup

setup(
    name='talos-te-clamSearch',
    version='0.2',
    packages=["clam", "clam.common"],
    description='TE ClamAV Search & Drop Tool',
    author='Will Koester',
    author_email='wikoeste@cisco.com',
    url='https://github.com/wikoeste/talos-te-clamsearch.git',
    entry_points={
        'console_scripts':[
            'talos-te-clamSearch=clam.main:main',
            ],
        },
)