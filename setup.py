from setuptools import setup

setup(
    name="comp0034-week10",
    packages=["paralympic_app", "iris_app", "paralympic_dash_app"],
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
        "sklearn",
    ],
)
