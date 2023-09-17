
<h2 align="center">Lottery Backend Application</h2>
This project contains implementation of a lottery backend application.
It allows users registers themselves to the system and submit ballots for specific days.
Every midnight, the lottery is drawn, and a winner ballot is chosen pseudo randomly.

<h3>Requirements:</h3>
**Python 3.11.0** to install package. 

Library dependencies are provided in **requirements.txt** and **requirements-dev.txt** files.

<h3> Installation & Execution </h3>
The application is provided with an installation package.
The user needs to execute the following command to install the application:

```
  pip install lottery_backend-0.0.1-py3-none-any.whl
  lottery_backend
```

---
<h4 align="center">Coding Style and Tools:</h4>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/black-000000.svg"></a>
<a href="https://github.com/PyCQA/flake8"><img alt="flake8" src="https://img.shields.io/badge/flake8-000000.svg"></a>
<a href="https://github.com/PyCQA/prospector"><img alt="prospector" src="https://img.shields.io/badge/prospector-000000.svg"></a>
<a href="https://github.com/pytest-dev/pytest"><img alt="pytest" src="https://img.shields.io/badge/pytest-000000.svg"></a>
<a href="https://github.com/pytest-dev/pytest-cov"><img alt="pytest-cov" src="https://img.shields.io/badge/pytest_cov-000000.svg"></a>
<a href="https://github.com/pytest-dev/pytest-bdd"><img alt="pytest-bdd" src="https://img.shields.io/badge/pytest_bdd-000000.svg"></a>
<a href="https://github.com/pytest-dev/pytest-mock"><img alt="pytest-mock" src="https://img.shields.io/badge/pytest_mock-000000.svg"></a>
<a href="https://github.com/ktosiek/pytest-freezegun"><img alt="pytest-freezegun" src="https://img.shields.io/badge/pytest_freezegun-000000.svg"></a>
<a href="https://github.com/python/mypy"><img alt="mypy" src="https://img.shields.io/badge/mypy-000000.svg"></a>
---

<h3> List of Endpoints </h3>

The application is accessible via 127.0.0.1:8000.
The list of endpoints can be viewed via "127.0.0.1:8000/docs" or "127.0.0.1:8000/redoc"
The OpenAPI endpoint is at "127.0.0.1:8000/openapi.json"
that allows the user to see all the details of endpoints as a json content.
The publicly available endpoints are as follows:

1. **/auth/token** => lets the user login to the lottery system

2. **/user/register** => allows user to register herself to the lottery system

3. **/ballot/submit** => enables user to submit a ballot for a specific day

4. **/ballot/list** => returns the list of submitted ballots on a specific day

5. **/ballot/winner** => returns the winner ballot of a specific day


<h3> Brief Explanation of the Application </h3>

Lottery Backend Application is implemented using Python 3.11.
As the backend framework, FastAPI is utilized.
Apart from the endpoints, a background process executes a scheduled task.
The lottery draw task is scheduled to take place every midnight for the previous day.
Out of the submitted ballots, one is randomly selected as the winner ballot.


<h4> Note: A ballot is designed to be a 16-digit array. 
For incorrect ballots, service returns with an HTTP error code 412.</h4>


<h3> Steps to Create a Wheel Installation Package </h3>

```
python -m pip install setuptools --force-reinstall
python -m pip install setuptools_scm
python -m pip install -r requirements.txt
python -m pip install wheel
python setup.py bdist_wheel
```