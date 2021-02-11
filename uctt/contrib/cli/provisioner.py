import logging
from typing import Dict, Any

import json

from configerus.config import Config

from uctt.cli import CliBase

logger = logging.getLogger('uctt.cli.provisioner')


class ProvisionerCliPlugin(CliBase):

    def fire(self, fixtures: Dict[str, Any]):
        """ return a dict of commands """
        return {
            'provisioner': ProvisionerGroup(fixtures['provisioner'])
        }


class ProvisionerGroup():

    def __init__(self, provisioner):
        self.provisioner = provisioner

    def prepare(self):
        """ Run provisioner prepare """
        self.provisioner.prepare()

    def apply(self):
        """ Run provisioner apply """
        self.prepare()
        self.provisioner.apply()

    def destroy(self):
        """ Run provisioner destroy """
        self.prepare()
        self.provisioner.destroy()
