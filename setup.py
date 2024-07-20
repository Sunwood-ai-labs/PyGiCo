from setuptools import setup

setup(
    name="pygico-imagegen",
    version="0.1.0",
    packages=["pygico_imagegen"],
    package_data={
        "pygico_imagegen": ["py.typed"],
    },
    include_package_data=True,
)
