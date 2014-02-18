import os

if not 'VIRTUAL_ENV' in os.environ:
    raise ValueError("You must run inside a virtualenv")

VIRTUAL_ENV = os.environ['VIRTUAL_ENV']

# VIRTUAL_ENV = '/usr/lib/ckan/default/bin/'

# ## Allow setting from the environment
# if 'VIRTUAL_ENV' in os.environ:
#     VIRTUAL_ENV = os.environ['VIRTUAL_ENV']

# print("Using virtualenv: {}".format(VIRTUAL_ENV))

# activate_this = os.path.join(VIRTUAL_ENV, 'bin/activate_this.py')
# execfile(activate_this, dict(__file__=activate_this))

## Now we have the path set up correctly and we can start loading
## the application..

from paste.deploy import loadapp

# here = os.path.dirname(os.path.abspath(__file__))
# config_filepath = os.path.join(here, 'production.ini')

if 'CKAN_CONFIG' in os.environ:
    config_filepath = os.path.abspath(os.environ['CKAN_CONFIG'])
else:
    config_filepath = os.path.join(VIRTUAL_ENV, 'etc/ckan/production.ini')

print("Configuration file: {}".format(config_filepath))

## Configure logging
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)

## Get the application
application = loadapp('config:%s' % config_filepath)

## Load configuration
from pylons import config

## Make sure this is configured properly

## --- NOTE ---
## it looks like full_stack is removed somewhere, so let's
## just hope for the best..

# if config.get('full_stack') != 'false':
#     raise ValueError("You must set full_stack = false in main configuration!")  # noqa

## Configure raven Sentry client
from raven import Client
from raven.middleware import Sentry

if 'SENTRY_DSN' in os.environ:
    sentry_dsn = os.environ['SENTRY_DSN']
else:
    sentry_dsn = config.get('sentry.dsn')

client = Client(sentry_dsn)
application = Sentry(application, client=client)

## This is to make sure 404 are redirected to a page that looks nice,
## normally done by setting full_stack = True
from pylons.middleware import StatusCodeRedirect
application = StatusCodeRedirect(application, [400, 404, 500])

## Configure logging
import logging
from raven.handlers.logging import SentryHandler

handler = SentryHandler(sentry_dsn)
handler.setLevel(logging.NOTSET)

loggers = ['', 'ckan', 'ckanext', 'sentry.errors']
for name in loggers:
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

## Just for debugging purposes..
ckan_logger = logging.getLogger('ckan')
ckan_logger.info("Sentry configured for this ckan instance (INFO)")
ckan_logger.warning("Sentry configured for this ckan instance (WARN)")
