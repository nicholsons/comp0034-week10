from setuptools import setup

setup(
    name="paralympic_app",
    packages=["paralympic_app", "iris_app"],
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-wtf",
        "flask-sqlalchemy",
        "Flask-WTF",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "pandas",
        "requests",
    ],
)

# Use the following version for the Iris ML app
"""
setup(
    name="iris_app",
    packages=["iris_app"],
    include_package_data=True,
    install_requires=[
        "flask",
        "pandas",
        "sklearn"
    ],
)
"""
