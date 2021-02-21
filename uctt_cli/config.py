import logging
from typing import Dict, Any

import json

from configerus.loaded import LOADED_KEY_ROOT

from uctt.environment import Environment
from uctt.cli import CliBase

logger = logging.getLogger('uctt.cli.config')


class ConfigCliPlugin(CliBase):

    def fire(self):
        """ return a dict of commands """
        return {
            'config': ConfigGroup(self.environment)
        }


class ConfigGroup():

    def __init__(self, environment: Environment):
        self.environment = environment

    def loaded(self, raw: bool = False):
        """ List loaded config labels """
        loaded = self.environment.config.loaded
        value = list(loaded)
        if raw:
            return value
        else:
            return json.dumps(value)

    def get(self, label: str, key: str = LOADED_KEY_ROOT, raw: bool = False):
        """ Retrieve configuration from the config object

        USAGE:

            uctt config get [--raw=True] {label} [{key}]


        """
        try:
            loaded = self.environment.config.load(label)
        except KeyError as e:
            return "Could not find the config label '{}'".format(label)

        try:
            value = loaded.get(key, exception_if_missing=True)
            if raw:
                return value
            else:
                return json.dumps(value, indent=2)
        except KeyError as e:
            return "Could not find the config key '{}'".format(key)

    def format(self, data: str,
               default_label: str = 'you did not specify a default', raw: bool = False):
        """ Format a target string using config templating """

        try:
            value = self.environment.config.format(
                data=data, default_label=default_label)
        except Exception as e:
            return "Error occured in formatting: '{}'".format(e)

        if raw:
            return value
        else:
            return json.dumps(value, indent=2)
