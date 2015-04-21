#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bulbs
import importlib

from flask import current_app


class Bulbs(object):

    db_types = ['neo4jserver', 'rexster']
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = app.config.copy()

        config.setdefault('BULBS_DATABASE', 'rexster')
        config.setdefault('BULBS_URI', 'http://localhost:8182/graphs/emptygraph')
        config.setdefault('BULBS_USER', None)
        config.setdefault('BULBS_PASSWORD', None)
        config.setdefault('BULBS_LOG_LEVEL', 'INFO')
        config.setdefault('BULBS_CONFIG', {})

        app.extensions.setdefault('bulbs', {})
        app.extensions['bulbs'][self] = self._get_graph(config)

    def _get_graph(self, config):
        """Get bulbs Graph based an app settings."""
        assert config['BULBS_DATABASE'] in self.db_types, \
            "Valid values for 'BULBS_DATABASE' are: %r" % self.db_types
        assert config['BULBS_LOG_LEVEL'] in self.log_levels, \
            "Valid values for 'BULBS_LOG_LEVEL' are: %r" % self.log_levels

        db = importlib.import_module('.%s' % config['BULBS_DATABASE'], 'bulbs')
        log_level = getattr(bulbs.config, config['BULBS_LOG_LEVEL'])

        bulbs_config = db.Config(
            config['BULBS_URI'],
            username=config['BULBS_USER'],
            password=config['BULBS_PASSWORD']
        )
        bulbs_config.set_logger(log_level)

        for key, value in config['BULBS_CONFIG'].iteritems():
            setattr(bulbs_config, key, value)

        return db.Graph(bulbs_config)

    @property
    def graph(self):
        app = self.app or current_app
        return app.extensions['bulbs'][self]
