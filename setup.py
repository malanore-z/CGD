import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="cgd",
    version="0.0.2",
    author="malanore.z",
    author_email="malanore.z@gmail.com",
    description="A auxiliary tool for algorithm competition questioner.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malanore-z/CGD",
    project_urls={
        "Bug Tracker": "https://github.com/malanore-z/CGD/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(".", include=("cgd", "cgd.*")),
    package_data={
        "cgd": ["resources/*"]
    },
    include_package_data=True,
    install_requires=[
        "zcommons",
    ],
    entry_points = {
        'console_scripts': [
            'cgd = cgd.cli_main:cgd',
        ],
    }
)
