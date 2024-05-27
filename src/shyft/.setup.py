from setuptools import setup, find_packages

# Reading the long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="shyft",
    version="0.0.2",
    packages=find_packages(where="src"),  # Find packages in 'src' directory
    package_dir={"": "src"},  # Root package directory is 'src'
    include_package_data=True,  # Automatically include package data
    author="Caleb Rice",
    author_email="caleb@coacts.com",
    description="shyft Logger is a simple CLI for tracking and managing contract services time records.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "shyft = shyft.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: >=3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click",  # Specify any other dependencies as needed
    ],
)
