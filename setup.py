import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="jendobson.greenbutton",
    version="0.0.2-c1",
    author="Jen Dobson",
    author_email="jendobson@gmail.com",
    description="Python tools to explore GreenButton data.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/JenDobson/greenbutton",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=[
        'xmlschema>=1.0',
        'pandas>=0.25',
        'matplotlib>=3.1',
    ],
    python_requires='>=3.7',
    keywords='greenbutton energy',
    package_data={
        'greenbutton': ['sample_data/*.xml'],
    }
    
)