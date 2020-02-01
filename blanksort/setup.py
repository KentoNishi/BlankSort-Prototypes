import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blanksort",
    version="0.0.1",
    author="KentoNishi",
    author_email="kento24gs@outlook.com",
    description="A Python package for BlankSort.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KentoNishi/BlankSort-Prototypes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)