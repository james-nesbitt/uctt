"""

Provisioning

"""

import logging

from configerus.config import Config

from .plugin import UCTTPlugin, Type

logger = logging.getLogger('uctt.provisioner')

UCTT_PLUGIN_TYPE_PROVISIONER = Type.PROVISIONER
""" Fast access to the Provisioner plugin_id """


class ProvisionerBase(UCTTPlugin):
    "Base Provisioner plugin class"

    def prepare(self):
        """ Prepare the provisioner to apply resources """
        pass

    def apply(self):
        """ bring a cluster to the configured state """
        pass

    def destroy(self):
        """ remove all resources created for the cluster """
        pass

    def get_output(self, name: str):
        """ retrieve an output from the provisioner """
        pass

    def get_client(self, type: str, index: str = ''):
        """ make a client of the type, and optionally of the index """
        pass
