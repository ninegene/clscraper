import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

config = {
    'name': 'CLScraper',
    'version': '0.1',
    'description': 'Craigslist Scraper',
    'long_description': '\n' + read('README.md'),
    'author': 'Aung L Oo',
    'author_email': 'aungloo@gmail.com',
    'url': 'https://github.com/ninegene/clscraper',
    'license': 'MIT',
    'packages': ['clscraper', 'tests'],
    'install_requires': [],
    'entry_points': {
        'console_scripts': [
            'clscraper = clscraper.__main__:main',
        ]
    }
}

setup(**config)