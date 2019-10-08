import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="jendobson.greenbutton",
    version="0.0.1",
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
    ],
    install_requires=[
        'xmlschema',
        'pandas',
        'matplotlib',
    ],
    python_requires='>=3.7',
        
    
)