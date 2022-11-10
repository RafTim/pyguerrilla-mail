from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = "A python guerrillamail client"
LONG_DESCRIPTION = "Python client which implements the guerrillamail API found at https://www.guerrillamail.com/GuerrillaMailAPI.html." \
                   "The guerrillamailer is itself open source and can be found at https://github.com/flashmob/go-guerrilla"


setup(
    name="pyguerrilla-mail",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Rafael Timmerberg",
    author_email="raffn1@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords="guerrilla mail",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10"
    ]
)
