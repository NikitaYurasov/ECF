from setuptools import setup, find_packages

with open("requirements.txt", "r") as fh:
    reqs = fh.read()

setup(
    name='pyecf',
    version="0.0.2",
    description='Elliptic Curve Factorization',
    python_requires='>=3.8',
    author='Yurasov Nikita',
    author_email='n.yurasov@yahoo.com',
    license='MIT',
    packages=find_packages(),
    install_requires=reqs,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/NikitaYurasov/ECF',
    include_package_data=True,
    zip_safe=False
)
