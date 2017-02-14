from setuptools import setup, find_packages

with open('description.txt') as f:
    long_description = ''.join(f.readlines())


def get_requirements():
    with open("requirements.txt") as f:
        return f.readlines()


setup(
    author="Martin Chovanec",
    author_email="chovamar@fit.cvut.cz",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    description="SacredBoard",
    long_description=long_description,
    license="MIT License",
    url="https://github.com/chovanecm/sacredboard",
    name="sacredboard",
    keywords="sacred",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "sacredboard = sacredboard.webapp:run"
        ]
    },
    install_requires=get_requirements(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    version="0.1"
)
