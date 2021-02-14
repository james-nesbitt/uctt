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
from uctt.provisioner import ProvisionerBase, UCTT_PROVISIONER_CONFIG_PROVISIONER_LABEL

from .base import DummyFixtures

logger = logging.getLogger('uctt.contrib.dummy.provisioner')


class DummyProvisionerPlugin(DummyFixtures, ProvisionerBase):
    """ Dummy provisioner class """

    def __init__(self, environment: Environment, instance_id: str, fixtures: Dict[str, Dict[str, Any]] = {}):
        """ Run the super constructor but also set class properties """
        ProvisionerBase.__init__(self, environment, instance_id)
        DummyFixtures.__init__(self, environment, fixtures)

    def apply(self):
        """ pretend to bring a cluster up """
        logger.info("{}:execute: apply()".format(self.instance_id))

    def prepare(self):
        """ pretend to prepare the cluster """
        logger.info("{}:execute: prepare()".format(self.instance_id))

    def destroy(self):
        """ pretend to brind a cluster down """
        logger.info("{}:execute: destroy()".format(self.instance_id))
