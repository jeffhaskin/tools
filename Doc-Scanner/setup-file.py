# setup.py
from setuptools import setup, find_packages

setup(
    name="document_scanner",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "opencv-python",
        "numpy",
        "Pillow",
        "python-docx"
    ],
    python_requires=">=3.7",
)