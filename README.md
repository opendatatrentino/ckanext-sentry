# CkanExt-Sentry

Hooks the Sentry's raven plugin into ckan/pylons wsgi middleware chain.


## Usage

Refer to: http://raven.readthedocs.org/en/latest/config/pylons.html

- Install plugin, add ``sentry`` to enabled plugins list
- Add sentry configuration to main configuration file
- Add logging configuration (todo: fix the "11 args" issue)
- **todo:** there seems to be some issues with pylons 0.9.7
  (or is it due to some customization?)


## Configuration options

- ``sentry.dsn``
  The DSN for connecting to sentry

- ``sentry.load_method``
  Specify how to hook sentry client into middleware chain.
  Allowed values:

  - ``none`` do not hook sentry client
  - ``pylons`` (default) use the pylon's way
  - ``wsgi`` use the generic way for wsgi apps

- ``sentry.configure_logging``
  If set to "true" (default), will add logging configuration
  while adding middleware to application.
