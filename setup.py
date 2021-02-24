from setuptools import setup

setup(
    name = 'vault',
    version = '0.0.1',
    packages = ['vault'],
    entry_points = {
        'console_scripts': [
            'vault = vault.__main__:main'
        ]
    }
)
