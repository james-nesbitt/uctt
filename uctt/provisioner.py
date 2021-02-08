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

    def prepare(self, label: str = '', base: str = ''):
        """ Prepare the provisioner to apply resources

        Initial Provisioner plugin is expected to be of very low cost until
        prepare() is executed.  At this point the plugin should load any config
        and perform any validations needed.
        The plugin should not create any resources but it is understood that
        there may be a cost of preparation.

        Provisioners are expected to load a lot of config to self-program.
        Because of this, they allow passing of a configerus label for .load()
        and a base for .get() in case there is an alterante config source
        desired.

        """
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
