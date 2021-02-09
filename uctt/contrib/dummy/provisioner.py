"""

Dummy MTT provisioner plugin

A provisioner which doesn't do anything, but can still be configured to produce
various clients and outputs.  The provisioner has no significant requirements
and no impact.  Provisioning can be repeated or interupted without impact.

The dummy provisioner is entirely config based.  Use the prepare() method to
indicate an appropriate config source and the provisioner will do the rest. As
long as you match its config convention it can take care of itself.

Point it to some appropriate configuration and it will self-populate with
the appropriate plugins:

```
'dummy_provisioner': {
    'plugin_id': UCTT_PLUGIN_ID_DUMMY,
    'clients': {
        # configure a client of type dummy, with instance_id = one
        'one': {
            'plugin_id': 'dummy',
            'arguments': {
                'outputs': {
                    'one': {
                        'plugin_id': 'text',
                        'arguments': {
                            'text': "prov client one output one"
                        }
                    },
                    'two': {
                        'plugin_id': 'dict',
                        'arguments': {
                            'data': {
                                '1': {
                                    '1': "prov client one output two data one.one"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    'outputs': {
        # configure one output of type text, with instance_id = dummy
        'dummy': {
            'plugin_id': 'text',
            'arguments': {
                'text': "prov dummy output one"
            }
        }
    }
}
```

"""

import logging

from configerus.loaded import LOADED_KEY_ROOT
import uctt
from uctt.provisioner import ProvisionerBase
from uctt.plugin import Type
from uctt.output import UCTT_OUTPUT_CONFIG_OUTPUTS_KEY
from uctt.client import UCTT_CLIENT_CONFIG_CLIENTS_KEY

logger = logging.getLogger('uctt.contrib.dummy.provisioner')

UCTT_DUMMY_PROVISIONER_CONFIG_LABEL = 'provisioner'
""" What config label should be loaded to pull dummy clients and outputs """
UCTT_DUMMY_PROVISIONER_CONFIG_KEY_OUTPUTS = UCTT_OUTPUT_CONFIG_OUTPUTS_KEY
""" What config key should be loaded to pull dummy outputs """
UCTT_DUMMY_PROVISIONER_CONFIG_KEY_CLIENTS = UCTT_CLIENT_CONFIG_CLIENTS_KEY
""" What config key should be loaded to pull dummy clients """


class DummyProvisionerPlugin(ProvisionerBase):
    """ Dummy provisioner class """

    def prepare(
            self, label: str = UCTT_DUMMY_PROVISIONER_CONFIG_LABEL, base: str = LOADED_KEY_ROOT):
        """

        Interpret provided config and configure the object with outputs and
        clients based on config

        """
        logger.info("{}:execute: prepare()".format(self.instance_id))

        if base == LOADED_KEY_ROOT:
            clients_key = UCTT_DUMMY_PROVISIONER_CONFIG_KEY_CLIENTS
            outputs_key = UCTT_DUMMY_PROVISIONER_CONFIG_KEY_OUTPUTS
        else:
            clients_key = '{}.{}'.format(
                base, UCTT_DUMMY_PROVISIONER_CONFIG_KEY_CLIENTS)
            outputs_key = '{}.{}'.format(
                base, UCTT_DUMMY_PROVISIONER_CONFIG_KEY_OUTPUTS)

        self.clients = uctt.new_clients_from_config(
            config=self.config,
            label=label,
            base=clients_key)
        self.outputs = uctt.new_outputs_from_config(
            config=self.config,
            label=label,
            base=outputs_key)

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
