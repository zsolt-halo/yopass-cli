from setuptools import setup

setup(
    name="yopass-cli",
    version="0.1",
    py_modules=["cli"],
    install_requires=["requests", "sjcl", "Click"],
    entry_points="""
        [console_scripts]
        yopass-cli=cli:cli
    """,
)
