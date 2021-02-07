"""

Dummy MTT provisioner plugin

"""

import logging

import uctt
from uctt.provisioner import ProvisionerBase
from uctt.plugin import Type

logger = logging.getLogger('uctt.contrib.dummy.provisioner')

UCTT_DUMMY_PROVISIONER_CONFIG_LABEL = 'provisioner'
""" What config label should be loaded to pull dummy clients and outputs """
UCTT_DUMMY_PROVISIONER_CONFIG_KEY_OUTPUTS = 'outputs'
""" What config key should be loaded to pull dummy outputs """
UCTT_DUMMY_PROVISIONER_CONFIG_KEY_CLIENTS = 'clients'
""" What config key should be loaded to pull dummy clients """


class DummyProvisionerPlugin(ProvisionerBase):
    """ Dummy provisioner class """

    def prepare(self, label: str = UCTT_DUMMY_PROVISIONER_CONFIG_LABEL):
        """

        Interpret provided config and configure the object with outputs and
        clients based on config

        """
        logger.info("{}:execute: prepare()".format(self.instance_id))

        self.clients = uctt.new_clients_from_config(
            config=self.config,
            label=UCTT_DUMMY_PROVISIONER_CONFIG_LABEL,
            key=UCTT_DUMMY_PROVISIONER_CONFIG_KEY_CLIENTS)
        self.outputs = uctt.new_outputs_from_config(
            config=self.config,
            label=UCTT_DUMMY_PROVISIONER_CONFIG_LABEL,
            key=UCTT_DUMMY_PROVISIONER_CONFIG_KEY_OUTPUTS)

    def apply(self):
        """ pretend to bring a cluster up """
        logger.info("{}:execute: apply()".format(self.instance_id))

    def destroy(self):
        """ pretend to brind a cluster down """
        logger.info("{}:execute: destroy()".format(self.instance_id))

    def get_output(self, instance_id: str):
        """ Retrieve a dummy output """
        logger.info("{}:execute: get_output()".format(self.instance_id))
        if not self.outputs:
            raise ValueError(
                'No outputs have been added to the dummy provisioner')
        return self.outputs.get_plugin(instance_id=instance_id)

    def get_client(self, plugin_id: str = '', instance_id: str = ''):
        """ Make a client as directed by the provisioner config """
        logger.info("{}:execute: get_client()".format(self.instance_id))
        if not self.clients:
            raise ValueError(
                'No clients have been added to the dummy provisioner')
        return self.clients.get_plugin(
            plugin_id=plugin_id, instance_id=instance_id)
