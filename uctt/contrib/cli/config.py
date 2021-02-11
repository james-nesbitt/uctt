import logging
from typing import Dict, Any

import json

from configerus.config import Config

from uctt.cli import CliBase

logger = logging.getLogger('uctt.cli.config')


class ConfigCliPlugin(CliBase):

    def fire(self, fixtures: Dict[str, Any]):
        """ return a dict of commands """
        return {
            'config': ConfigGroup(fixtures['config'])
        }


class ConfigGroup():

    def __init__(self, config: Config):
        self.config = config

    def get(self, label: str, key: str, raw: bool = False):
        """ Retrieve configuration from the config object

        USAGE:

            uctt config get [--raw=True] {label} [{key}]


        """
        try:
            loaded = self.config.load(label)
        except KeyError as e:
            return "Could not find the config label '{}'".format(label)

        try:
            value = loaded.get(key, exception_if_missing=True)
            if raw:
                return value
            else:
                return json.dumps(value)
        except KeyError as e:
            return "Could not find the config key '{}'".format(key)
