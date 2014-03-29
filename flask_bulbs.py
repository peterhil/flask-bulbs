#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bulbs
import importlib

from flask import current_app

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Bulbs(object):

    db_types = ['neo4jserver', 'rexster']
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('BULBS_DATABASE', 'rexster')
        app.config.setdefault('BULBS_URI', 'http://localhost:8182/graphs/emptygraph')
        app.config.setdefault('BULBS_USER', None)
        app.config.setdefault('BULBS_PASSWORD', None)
        app.config.setdefault('BULBS_LOG_LEVEL', 'INFO')
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def get_graph(self):
        """Get bulbs Graph based an app settings."""
        assert current_app.config['BULBS_DATABASE'] in self.db_types, "Valid values for 'BULBS_DATABASE' are: %r" % self.db_types
        assert current_app.config['BULBS_LOG_LEVEL'] in self.log_levels, "Valid values for 'BULBS_LOG_LEVEL' are: %r" % self.log_levels

        db = importlib.import_module('.%s' % current_app.config['BULBS_DATABASE'], 'bulbs')
        log_level = getattr(bulbs.config, current_app.config['BULBS_LOG_LEVEL'])

        config = db.Config(
            current_app.config['BULBS_URI'],
            username=current_app.config['BULBS_USER'],
            password=current_app.config['BULBS_PASSWORD'],
        )
        config.set_logger(log_level)

        return db.Graph(config)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'graph'):
            ctx.graph = None

    @property
    def graph(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'graph'):
                ctx.graph = self.get_graph()
            return ctx.graph
