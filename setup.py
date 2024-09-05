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
        "httpx==0.24.0",
        "pytest-cov==4.0.0"  # Optional, if you want test coverage reporting
    ],
    entry_points={
        "console_scripts": [
            "runserver=app.main:main"  # Adjust as needed
        ]
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Specify the minimum Python version
)
