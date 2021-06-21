import os

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('menuController.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "MealDeal-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    ### end swagger specific ###

    # DB initialization
    from . import db
    db.init_app(app)

    # Blueprints
    from flaskr.Controllers import neuronalNetworkController
    app.register_blueprint(neuronalNetworkController.bp)

    from flaskr.Controllers import authController
    app.register_blueprint(authController.bp)

    from flaskr.Controllers import menuController
    app.register_blueprint(menuController.bp)
    app.add_url_rule('/', endpoint='index')

    return app
