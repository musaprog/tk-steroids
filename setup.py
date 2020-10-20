import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
        'tkinter',
        'PIL',
        'numpy',
        'matplotlib',
        ]

setuptools.setup(
    name="tk_steroids-jkemppainen", # Replace with your own username
    version="0.0.1",
    author="Joni Kemppainen",
    author_email="jjtkemppainen1@sheffield.ac.uk",
    description="A collection of custom tkinter bits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jkemppainen/tk_steroids",
    packages=setuptools.find_packages(),
    install_requires=install_requires
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3) ",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
