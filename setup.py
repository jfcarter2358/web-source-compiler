import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("wsc/VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().split('\n')

setuptools.setup(
    name="web-source-compiler",
    version=version,
    author="John Carter",
    author_email="jfcarter2358@gmail.com",
    description="A package for reading Jenkinsfile-like pipeline files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfcarter2358/web-source-compiler",
    entry_points={
        "console_scripts": ["wsc = wsc.wsc:main"],
    },
    project_urls={
        "Bug Tracker": "https://github.com/jfcarter2358/web-source-compiler/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
)
