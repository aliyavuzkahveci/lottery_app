#!/usr/bin/env python
import os
import sys
from pathlib import Path

from setuptools import setup

from lottery_backend.version import __version__

CURRENT_DIR = Path(__file__).parent
LIBRARY_NAME = "lottery_backend"
sys.path.insert(0, str(CURRENT_DIR))


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


extra_files = package_files(os.path.join(CURRENT_DIR, LIBRARY_NAME))

setup(
    name=LIBRARY_NAME,
    version=__version__,
    description="Lottery Backend Service",
    long_description=f"{get_long_description()}\n\n",
    author="Ali Yavuz Kahveci",
    author_email="aliyavuzkahveci@gmail.com",
    url="",
    packages=[LIBRARY_NAME],
    package_data={"": extra_files},
    zip_safe=False,
    keywords=LIBRARY_NAME,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
    ],
    license="",
    test_suite="test",
    install_requires=[
        "annotated-types==0.5.0",
        "anyio==3.7.1",
        "bcrypt==4.0.1",
        "certifi==2023.7.22",
        "click==8.1.7",
        "colorama==0.4.6",
        "dnspython==2.4.2",
        "email-validator==2.0.0.post2",
        "fastapi==0.101.1",
        "greenlet==2.0.2",
        "h11==0.14.0",
        "httpcore==0.17.3",
        "httptools==0.6.0",
        "httpx==0.24.1",
        "idna==3.4",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.2",
        "MarkupSafe==2.1.3",
        "orjson==3.9.5",
        "passlib==1.7.4",
        "pydantic==1.10.12",
        "python-dotenv==1.0.0",
        "python-multipart==0.0.6",
        "PyYAML==6.0.1",
        "schedule==1.2.0",
        "sniffio==1.3.0",
        "SQLAlchemy==1.4.41",
        "sqlalchemy2-stubs==0.0.2a35",
        "sqlmodel==0.0.8",
        "starlette==0.27.0",
        "structlog==23.1.0",
        "typing_extensions==4.7.1",
        "ujson==5.8.0",
        "uvicorn==0.23.2",
        "watchfiles==0.19.0",
        "websockets==11.0.3",
    ],
    setup_requires=[],
    tests_require=[],
    extras_require={
        "dev": [
            "astroid==2.15.6",
            "black==23.7.0",
            "cfgv==3.4.0",
            "coverage==7.3.0",
            "dill==0.3.7",
            "distlib==0.3.7",
            "dodgy==0.2.1",
            "filelock==3.12.2",
            "flake8==5.0.4",
            "flake8-polyfill==1.0.2",
            "gitdb==4.0.10",
            "GitPython==3.1.32",
            "identify==2.5.27",
            "iniconfig==2.0.0",
            "isort==5.12.0",
            "lazy-object-proxy==1.9.0",
            "mccabe==0.7.0",
            "mypy==1.5.1",
            "mypy-extensions==1.0.0",
            "nodeenv==1.8.0",
            "packaging==23.1",
            "pathspec==0.11.2",
            "pep8-naming==0.10.0",
            "platformdirs==3.10.0",
            "pluggy==1.2.0",
            "pre-commit==3.3.3",
            "prospector==1.10.2",
            "pycodestyle==2.9.1",
            "pydocstyle==6.3.0",
            "pyflakes==2.5.0",
            "pylint==2.17.5",
            "pylint-celery==0.3",
            "pylint-django==2.5.3",
            "pylint-flask==0.6",
            "pylint-plugin-utils==0.7",
            "pytest==7.4.0",
            "pytest-asyncio==0.21.1",
            "requirements-detector==1.2.2",
            "semver==3.0.1",
            "setoptconf-tmp==0.3.1",
            "smmap==5.0.0",
            "snowballstemmer==2.2.0",
            "toml==0.10.2",
            "tomlkit==0.12.1",
            "virtualenv==20.24.3",
            "wrapt==1.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lottery_backend=lottery_backend.main:main",
        ],
    },
)
