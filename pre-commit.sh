#!/bin/bash
black --check .
flake8 . --isolated --ignore=E402,E501
pytest -ra --cov=./