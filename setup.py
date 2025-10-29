from setuptools import setup, find_packages

setup(
    name="py2dll",
    version="1.0",
    author="ethanmal30",
    description="Convert Python file(s) to DLL file(s).",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["cython>=0.29"],
    python_requires=">=3.13",
    entry_points={
        "console_scripts": [
            "py2dll=py2dll.__main__:main",
        ],
    },
)