import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yopass-cli",
    version="0.0.2",
    author="Zsolt Halo",
    author_email="net.zsolt.net@gmail.com",
    description="A cli for interacting with yopass backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zsolt-halo/yopass-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "sjcl", "click"],
    entry_points="""
        [console_scripts]
        yopass-cli=cli.cli:cli
    """,
)
