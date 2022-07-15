# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask

app = Flask(__name__)
from . import forms, routes

def create_app(config, boba_machine):
    app.config.from_object(config)
    app.boba_machine = boba_machine
    return app
