from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name="WebaltoPositioning",
    version="1.0.0",
    author="YunWenKu",
    author_email="yun-wen.ku@amundi.com",
    description="Python package to download positioning data from webalto",
    long_description = long_description,
    packages=find_packages()
)