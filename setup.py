from setuptools import setup

VERSION = '0.1'

long_description = ''

setup(
    name='permissions',
    version=VERSION,
    description='',
    long_description=long_description,
    url='https://github.com/gpiantoni/umcu-metc',
    author="Gio Piantoni",
    author_email='permissions@gpiantoni.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    keywords='analysis',
    install_requires=[
        '',  # pyqt5
        ],
    entry_points={
        'console_scripts': [
            'create_database_permissions=permissions.command:create_database_permissions',
            'add_permissions=permissions.command:add_permissions',
            'get_permissions=permissions.command:get_permissions',
        ],
    },
    )
