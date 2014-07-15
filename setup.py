import os.path
from pip.req import parse_requirements

try:
    from setuptools import find_packages, setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import find_packages, setup


def readfile(filename):
    try:
        with open(os.path.join(os.path.dirname(__file__), filename)) as f:
            return f.read()
    except (IOError, OSError):
        return ''


install_reqs = [str(ir.req) for ir in parse_requirements('requirements.txt')]


setup(
    name='karaokeserver',
    description='Database update server for KaraokeBook',
    long_description=readfile('README.md'),
    url='http://kjwon15.net/',
    download_url='https://github.com/Kjwon15/karaoke-server/releases',
    author='Kjwon15',
    author_email='kjwonmail@gmail.com',
    entry_points={
        'console_scripts': [
            'karaoke-server = karaokeserver.command:main'
        ]
    },
    packages=find_packages(),
    install_requires=install_reqs,
)
