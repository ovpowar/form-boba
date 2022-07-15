# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask_migrate import Migrate
from sys import exit
from apps import create_app
from apps.config import config_dict
from BobaHardware import BobaMachine

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'
try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
boba_machine = BobaMachine()
app = create_app(app_config, boba_machine)

if __name__ == "__main__":
    app.run()
