from setuptools import setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

import checkmem

setup(
    name="sample",
    version=checkmem.__version__,
    url="https://github.com/pietrogiuffrida/checkmem/",
    author="Pietro Giuffrida",
    author_email="pietro.giuffri@gmail.com",
    license="MIT",
    packages=["checkmem"],
    zip_safe=False,
    install_requires=['pandas', 'requests', 'psutil'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Manage a list of names with several "
                "properties and (overlapping) order criteria",
    # long_description=long_description,
    long_description_content_type="text/markdown",
)
