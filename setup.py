from setuptools import setup, find_packages

setup(
    name='Alpheios Web App',
    version='0.0.1',
    long_description="No long description atm",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
