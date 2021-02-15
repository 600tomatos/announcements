import os
import logging

from flask import Flask
from lambdas.helpers.utils.cors import CORS

from lambdas.resources.api import upgrade_app

# Set base logging config
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Basic Configuration class for an Application
class AppConfig:
    ERROR_404_HELP = False
    RESTX_MASK_SWAGGER = False
    STAGE = os.getenv("STAGE")


app = CORS(Flask(__name__))
app.config.from_object(AppConfig())
upgrade_app(app)
