!/bin/sh

"""Separate the packages needed for dev and prod:

    dev: These are only used for development (e.g., testing, linting, etc.) and are not required for production.
    prod: These are needed in production (e.g., data processing, machine learning, etc.).
"""

# Install dev packages which we'll use for testing, linting, type-checking etc.
pip install pytest pytest-cov pylint mypy codecov

# Freeze dev requirements
pip freeze > requirements.dev

# Install prod packages
pip install python

# Freeze dev requirements
pip freeze > requirements.prod