# Flask Management Blueprint

[![Build Status](https://travis-ci.org/stone-payments/flask-management-blueprint.svg?branch=master)](https://travis-ci.org/stone-payments/flask-management-blueprint)

This repository contains a project developed with Python3 :heart: with a blueprint that describe the necessary endpoints to meet the engineering goals.

## Starting

This instructions should be enough to replicate the development enviroment of this project. If this is not the case, please, feel free to open a pull request.

## Prerequisites

After cloning the project, you will need Python 3.5.

## Environment

```bash
python3 -m venv /path/to/new/virtual/environment
source venv/bin/activate
pip install -r requirements.txt
```

## Settings

To successfully set up the project, a json file is needed. This file should be in path described in the enviroment variable CONFIG_FILE_PATH.

Besides that, all of the project's dependencies should be added with the `AppInfo`'s method `register_resource`. This method should receive a function that returns `True` or `False` depending on the dependency's health.

## Running

If all goes right, you should be run the `run.py` file inside the samples folder.

## Testing

Unit tests:

`nosetests tests/unit`

Coverage:

`nosetests --with-coverage --cover-package=flask_management_blueprint`

## Built With

Python 3.5.2

## Authors

Build with :heart: by Team Satisfação do Cliente!

## License

Copyright (C) 2018. Stone Pagamentos. All rights reserved.
