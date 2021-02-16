import logging
from typing import Dict, Any

import json

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.cli import CliBase

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

    def _select_provisioner(self, instance_id: str = ''):
        """ Pick a matching provisioner """
        if instance_id:
            return self.environment.fixtures.get_plugin(
                type=Type.PROVISIONER, instance_id=instance_id)
        else:
            # Get the highest priority provisioner
            return self.environment.fixtures.get_plugin(type=Type.PROVISIONER)

    def prepare(self, provisioner: str = ''):
        """ Run provisioner prepare """
        provisioner = self._select_provisioner(instance_id=provisioner)
        provisioner.prepare()

    def apply(self, provisioner: str = ''):
        """ Run provisioner apply """
        provisioner = self._select_provisioner(instance_id=provisioner)
        provisioner.prepare()
        provisioner.apply()

    def destroy(self, provisioner: str = ''):
        """ Run provisioner destroy """
        provisioner = self._select_provisioner(instance_id=provisioner)
        provisioner.prepare()
        provisioner.destroy()
