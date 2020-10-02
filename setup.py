import setuptools

setuptools.setup(
    name = 'Windows-Screensaver',
    version = '1.1.0',
    url = 'https://github.com/gaming32/Windows-Screensaver',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'Simple library for creating Windows screensavers',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    install_requires = [
        'pywin32'
    ],
    py_modules = [
        'winscr',
    ],
)
