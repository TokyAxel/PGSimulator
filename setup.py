import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PGSimulator",
    version="0.1.0",
    author="RASOANAIVO Andry, ANDRIAMALALA Rahamefy Solofohanitra, ANDRIAMIZAKASON Toky Axel",
    author_email="tokyandriaxel@gmail.com",
    description="A Power Grid Simulator to calculate the least grid cost using optimizers from nevergrad package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TokyAxel/PGSimulator",
    packages=setuptools.find_packages(include=['PGSimulator', 'PGSimulator.*']),
    include_package_data=True,
    #package_data={'mixsimulator': ['data/RIToamasina/dataset_RI_Toamasina.csv']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

