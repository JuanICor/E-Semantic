from setuptools import setup, find_packages

setup(
    name= "JI Rules",
    version= "0.0.1", 
    packages= find_packages(),
    install_requieres= [
        'egglog>=7.2.0'
    ],
    author= "Juan Ignacio Cortez",
    author_email= "juan.cortez@mi.unc.edu.ar",
    )