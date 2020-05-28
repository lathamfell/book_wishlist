from environs import Env

env = Env()
env.read_env()

LOG_LEVEL = env.str("LOG_LEVEL", "debug")
DEBUG = env.bool("FLASK_DEBUG", True)
