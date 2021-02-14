import logging
from typing import Dict, Any

import json

from uctt import environment_names
from uctt.environment import Environment
from uctt.cli import CliBase

logger = logging.getLogger('uctt.cli.environment')


class EnvironmentCliPlugin(CliBase):

    def fire(self):
        """ return a dict of commands """
        return {
            'environment': EnvironmentGroup(self.environment)
        }


class EnvironmentGroup():

    def __init__(self, environment: Environment):
        self.environment = environment

    def names(self, raw: bool = False):
        """ List all of the environment names  """
        names = environment_names()
        if raw:
            return names
        else:
            return json.dumps(names)
