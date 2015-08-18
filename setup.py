from distutils.core import setup

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''

setup(
    name='pg4nosql',
    version='0.3.3',
    packages=['pg4nosql'],
    url='https://github.com/cansik/pg4nosql',
    license='MIT License',
    author='Florian Bruggisser',
    author_email='florian@nexpose.ch',
    description='A simple psycopg2 based wrapper for nosql like database interaction with python.',
    long_description=description,
    download_url='https://github.com/cansik/pg4nosql/tarball/0.3.3',
    keywords=['postgres', 'nosql', 'wrapper', 'database', 'json'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)
