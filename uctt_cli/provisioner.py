import logging
from typing import Dict, Any

import json

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.cli import CliBase

from .output import OutputGroup

logger = logging.getLogger('uctt.cli.provisioner')


class ProvisionerCliPlugin(CliBase):

    def fire(self):
        """ return a dict of commands """
        return {
            'provisioner': ProvisionerGroup(self.environment)
        }


class ProvisionerGroup():

    def __init__(self, environment: Environment):
        self.environment = environment

    def list(self, raw: bool = False):
        """ List all provisioners """
        list = [
            plugin.instance_id for plugin in self.environment.fixtures.get_plugins(
                type=Type.PROVISIONER)]

        if raw:
            return list
        else:
            return json.dumps(list)

    def _select_provisioner(self, instance_id: str = ''):
        """ Pick a matching provisioner """
        if instance_id:
            return self.environment.fixtures.get_fixture(
                type=Type.PROVISIONER, instance_id=instance_id)
        else:
            # Get the highest priority provisioner
            return self.environment.fixtures.get_fixture(type=Type.PROVISIONER)

    def info(self, provisioner: str = ''):
        """ get info about a provisioner plugin """
        fixture = self._select_provisioner(instance_id=provisioner)

        provisioner_info = {
            'fixture': {
                'type': fixture.type.value,
                'plugin_id': fixture.plugin_id,
                'instance_id': fixture.instance_id
            }
        }

        if hasattr(fixture.plugin, 'info'):
            provisioner_info.update(fixture.plugin.info())

        return json.dumps(provisioner_info, indent=2)

    def output(self, output: str, provisioner: str = ''):
        """ Interact with provisioner outputs """
        provisioner = self._select_provisioner(instance_id=provisioner).plugin
        if not hasattr(provisioner, 'get_output'):
            raise ValueError('This provisioner does not keep outputs.')

        plugin = provisioner.get_output(instance_id=output)

        if not hasattr(plugin, 'get_output'):
            raise ValueError(
                "Found output '{}' but is cannot be exported in the cli.".format(
                    plugin.instance_id))

        json.dumps(plugin.get_output(), indent=2)

    def fixtures(self, provisioner: str = ''):
        """ List all outputs """
        provisioner = self._select_provisioner(instance_id=provisioner).plugin
        if not hasattr(provisioner, 'get_fixtures'):
            raise ValueError('This provisioner does not keep fixtures.')
        list = [{
            'type': fixture.type.value,
            'plugin_id': fixture.plugin_id,
            'instance_id': fixture.instance_id,
            'priority': fixture.priority,
        } for fixture in provisioner.get_fixtures().to_list()]

        json.dumps(list, indent=2)

    def prepare(self, provisioner: str = ''):
        """ Run provisioner prepare """
        provisioner = self._select_provisioner(instance_id=provisioner).plugin
        provisioner.prepare()

    def apply(self, provisioner: str = ''):
        """ Run provisioner apply """
        provisioner = self._select_provisioner(instance_id=provisioner).plugin
        provisioner.apply()

    def destroy(self, provisioner: str = ''):
        """ Run provisioner destroy """
        provisioner = self._select_provisioner(instance_id=provisioner).plugin
        provisioner.destroy()
