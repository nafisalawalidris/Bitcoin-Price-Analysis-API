from setuptools import setup, find_packages

setup(
    name="bitcoin-price-analysis-api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.95.0",
        "uvicorn==0.22.0",
        "sqlalchemy==1.4.47",
        "psycopg2-binary==2.9.6",
    ],
    tests_require=[
        "pytest==7.4.2",
        "httpx==0.24.0"
    ],
    entry_points={
        "console_scripts": [
            "runserver=app.main:app"
        ]
    }
)
