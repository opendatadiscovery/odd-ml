#!/bin/bash
pytest
black .
isort --profile black .