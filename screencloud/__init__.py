from . import config

# Setup config (this prevents access to the config module here too)
config = config.to_dict()
