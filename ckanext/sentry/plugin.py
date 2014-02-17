# -*- coding: utf-8 -*-

from ckan.plugins import implements, SingletonPlugin, IMiddleware


class ApiNgPlugin(SingletonPlugin):
    implements(IMiddleware)

    def make_middleware(self, app, config):
        app = self._add_sentry(app, config)
        if config.get('sentry.configure_logging', 'true').lower() == 'true':
            self._configure_logging(config)
        return app

    def _add_sentry(self, app, config):
        alternative = config.get('sentry.load_method', 'pylons')
        if alternative == 'none':
            return
        if alternative == 'pylons':
            return self._add_sentry_pylons(app, config)
        if alternative == 'wsgi':
            return self._add_sentry_wsgi(app, config)
        raise ValueError("Invalid sentry.load_method. "
                         "Supported: none, pylons, wsgi. Got: {0}"
                         .format(alternative))

    def _add_sentry_pylons(self, app, config):
        """Use pylons-specific sentry configuration"""

        from raven.contrib.pylons import Sentry
        return Sentry(app, config)

    def _add_sentry_wsgi(self, app, config):
        """Fallback to pure wsgi"""

        from raven.middleware import Sentry
        from raven import Client
        client = Client(config.get('sentry.dsn'))
        return Sentry(app, client)

    def _configure_logging(self, config):
        """Configure loggers here, to hook sentry handler"""

        import logging
        from raven.handlers.logging import SentryHandler

        handler = SentryHandler(config.get('sentry.dsn'))
        handler.setLevel(logging.NOTSET)

        loggers = ['', 'ckan', 'ckanext', 'sentry.errors']
        for name in loggers:
            logger = logging.getLogger(name)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        ckan_logger = logging.getLogger('ckan')
        ckan_logger.info("Sentry configured for this ckan instance (INFO)")
        ckan_logger.warning("Sentry configured for this ckan instance (WARN)")
