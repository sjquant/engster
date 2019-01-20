from .base import *

# load env
load_dotenv(os.path.join(ENVDIR, 'secrets/.env.test'))

ENV = 'test'
DEBUG = True

BCRYPT_LOG_ROUNDS = 6
