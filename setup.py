try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': "This tool creates RoadMiles by State by Grid Cell",
    'author': "Murtaza Nasafi",
    'author_email': "murtaza.nasafi@fcc.gov",
    'version': '0.1',
    'install_requires': ['nose', 'arcpy', 'pandas', 'numpy'],
    'packages': ['GRIDTERRAIN'],
    'scripts': [],
    'name': 'TheRoadWarrior'
}

setup(**config)
