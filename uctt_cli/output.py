import logging
from typing import Dict, Any, List

import json

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.cli import CliBase

logger = logging.getLogger('uctt.cli.output')


class OutputCliPlugin(CliBase):

    def fire(self):
        """ return a dict of commands """
        return {
            'output': OutputGroup(self.environment)
        }


class OutputGroup():

    def __init__(self, environment: Environment, output_list_limit: List[str] = []):
        self.environment = environment
        self.output_list_limit = output_list_limit
        """ limits operations to output instance_ids in this list so that this can be subclassed """

    def list(self, raw: bool = False):
        """ List all outputs """
        list = [plugin.instance_id for plugin in self.environment.fixtures.get_plugins(type=Type.OUTPUT) if len(self.output_list_limit)==0 or plugin.instance_id in self.output_list_limit]

        if raw:
            return list
        else:
            return json.dumps(list)
