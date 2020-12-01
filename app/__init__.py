from flask import Flask

from app.api.bought import bought
from app.api.controllerRGB import rgb
from app.api.device_overview import dev
from app.api.status import status
from app.api.wishlist import wish
from app.auth import auth
from app.gui.bought import bought as bought_gui
from app.gui.controllerRGB import rgb as rgb_gui
from app.gui.device_overview import device as device_gui
from app.gui.index import index as index_gui
from app.gui.status import status as status_gui
from app.gui.wishlist import wish as wish_gui


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='yiQHZzmYOFvLJPXxWjIFIkNZKtVcXSDTDM70SGhKnBE526lW38GdbRARsNMeHgqraQ1uUpYL4PBfTAoJ9wCEVUOC',
    )

    app.register_blueprint(auth)
    app.register_blueprint(wish)
    app.register_blueprint(bought)
    app.register_blueprint(status)
    app.register_blueprint(rgb)
    app.register_blueprint(dev)

    app.register_blueprint(index_gui)
    app.register_blueprint(wish_gui)
    app.register_blueprint(bought_gui)
    app.register_blueprint(status_gui)
    app.register_blueprint(rgb_gui)
    app.register_blueprint(device_gui)

    return app


create_app().run()
