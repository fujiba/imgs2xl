import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setuptools.setup(
    name="imgs2xl",
    version="0.1.0",
    author="T.Fujiba",
    description="Output an Excel sheet with thumbnails from an image files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fujiba/imgs2xl",
    packages=setuptools.find_packages(),
    install_requires=install_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "imgs2xl = imgs2xl.imgs2xl:main",
        ],
        "gui_scripts": [
            "gimgs2xl = imgs2xl.gui:main",
        ],
    },
    python_requires=">=3.7",
)
