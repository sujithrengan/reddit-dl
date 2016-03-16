try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Reddit Image Scrapper',
    'author': 'Ratbag',
    'url': 'lol',
    'download_url': 'Unavailable',
    'author_email': 'thehyperion.projects@gmail.com',
    'version': '0.1',
    'install_requires': ['bs4','requests','praw','nose'],
    'packages': ['redditdl'],
    'scripts': [],
    'name': 'reddit-dl'
}

setup(**config)
