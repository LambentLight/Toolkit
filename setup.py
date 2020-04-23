from setuptools import setup


with open("README.md") as file:
    readme = file.read()

setup(
    name="lambentlight",
    version="1.0",
    author="Hannele 'Lemon' Ruiz",
    author_email="justlemoncl@gmail.com",
    description="Tools for working with the Metadata files of LambentLight",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/LambentLight/Toolkit",
    packages=["lambentlight"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing"
    ]
)
