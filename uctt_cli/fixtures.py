import logging
from typing import Dict, Any

import json

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.cli import CliBase

from .output import OutputGroup

logger = logging.getLogger('uctt.cli.fixtures')


class FixturesCliPlugin(CliBase):

    def fire(self):
        """ return a dict of commands """
        return {
            'fixtures': FixturesGroup(self.environment)
        }


class FixturesGroup():

    def __init__(self, environment: Environment):
        self.environment = environment

    def list(self, include_cli_plugins: bool = False):
        """ List all provisioners """
        list = [fixture.instance_id for fixture in self.environment.fixtures.get_fixtures(
        ).to_list() if include_cli_plugins or fixture.type is not Type.CLI]

        return json.dumps(list, indent=2)

    def details(self, type: str = '', plugin_id: str = '',
                instance_id: str = '', include_cli_plugins: bool = False):
        """ List all outputs """

        if type:
            type = Type.from_string(type)
        else:
            type = None

        list = [{
            'type': fixture.type.value,
            'plugin_id': fixture.plugin_id,
            'instance_id': fixture.instance_id,
            'priority': fixture.priority,
        } for fixture in self.environment.fixtures.get_fixtures(type=type, plugin_id=plugin_id, instance_id=instance_id).to_list() if include_cli_plugins or fixture.type is not Type.CLI]

        return json.dumps(list, indent=2)
