"""

Dummy MTT provisioner plugin

A provisioner which doesn't do anything, but can still be configured to produce
various clients and outputs.  The provisioner has no significant requirements
and no impact.  Provisioning can be repeated or interupted without impact.

The dummy provisioner is entirely config based.  Use the prepare() method to
indicate an appropriate config source and the provisioner will do the rest. As
long as you match its config convention it can take care of itself.

"""

import logging
from typing import Dict, Any

from uctt.plugin import Type
from uctt.environment import Environment

logger = logging.getLogger('uctt.contrib.dummy.base')


class DummyFixtures():
    """ Dummy provisioner class """

    def __init__(self, environment: Environment, fixtures: Dict[str, Dict[str, Any]] = {} ):
        """
        Parameters:
        -----------

        environment (Environment) : an environment in which we should create fixtures.

        fixtures (dict) : A plugin list of fixture definitions from which we should
            created fixtuers. Passed to environment.add_fixtures_from_config()

        """
        self.fixtures = environment.add_fixtures_from_dict(plugin_list=fixtures)
        """ All fixtures added to this dummy provisioner.  We will use outputs and clients """

    def get_output(self, plugin_id: str = '', instance_id: str = ''):
        """ Retrieve one of the passed in fixture outputs """
        return self.get_plugin(type=Type.OUTPUT, plugin_id=plugin_id, instance_id=instance_id)

    def get_client(self, plugin_id: str = '', instance_id: str = ''):
        """ Retrieve one of the passed in fixture clients """
        return self.get_plugin(type=Type.CLIENT, plugin_id=plugin_id, instance_id=instance_id)

    def get_workload(self, plugin_id: str = '', instance_id: str = ''):
        """ Retrieve one of the passed in fixture workloads """
        return self.get_plugin(type=Type.WORKLOAD, plugin_id=plugin_id, instance_id=instance_id)

    def get_plugin(self, type: Type = None, plugin_id: str = '', instance_id: str = ''):
        """ Retrieve one of the passed in fixtures """
        logger.info("{}:execute: get_plugin({})".format(self.instance_id, type.value))
        return self.fixtures.get_plugin(type=type, plugin_id=plugin_id, instance_id=instance_id)
