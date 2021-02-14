"""

Dummy client plugin

"""

import logging
from typing import Dict, Any

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.client import ClientBase

from .base import DummyFixtures

logger = logging.getLogger('uctt.contrib.dummy.client')

class DummyClientPlugin(DummyFixtures, ClientBase):
    """ Dummy client class

    As with all dummies, this is a failsafe plugin, that should never throw any
    exceptions if used according to mtt standards.

    It can be used as a placeholder during development, or it can be used to
    log client events and output for greater development and debugging.

    The client will log any method call, including unknown methods, and so it
    can be used in place of any client, if you don't need the methods to return
    anything
    """

    def __init__(self, environment: Environment, instance_id: str, fixtures: Dict[str, Dict[str, Any]] = {}):
        """ Run the super constructor but also set class properties

        Overrides the ClientBase.__init__

        Arguments:
        ----------

        environment (uctt.environment.Environment) : Environment in which this
            plugin exists.

        instance_id (str) : unique identifier for this plugin instance.

        fixtures (dict) : You can pass in some fixture definitions which this
            class will turn into fixtures and make retrievable.  This is a big
            part of the dummy.

        """
        ClientBase.__init__(self, environment, instance_id)
        DummyFixtures.__init__(self, environment, fixtures)
