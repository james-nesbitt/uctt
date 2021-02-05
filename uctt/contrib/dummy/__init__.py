"""

MTT Dummy

Dummy plugin functionality.  Various plugins that can be used as placeholders
and for testing.

"""

from configerus.config import Config

from uctt import plugin as uctt_plugin

from .plugins.provisioner import DummyProvisionerPlugin
from .plugins.client import DummyClientPlugin
from .plugins.workload import DummyWorkloadPlugin

UCTT_PLUGIN_ID_DUMMY = 'dummy'
""" All of the dummy plugins use 'dummy' as their plugin_id """

""" provisioner plugin_id for the mtt dummy plugin """
@uctt_plugin.Factory(type=uctt_plugin.Type.PROVISIONER, plugin_id=UCTT_PLUGIN_ID_DUMMY)
def uctt_plugin_factory_provisioner_dummy(config:Config, instance_id: str = ''):
    """ create an mtt provisionersss dict plugin """
    return DummyProvisionerPlugin(config, instance_id)

""" client plugin_id for the mtt dummy plugin """
@uctt_plugin.Factory(type=uctt_plugin.Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_DUMMY)
def uctt_plugin_factory_client_dummy(config:Config, instance_id: str = ''):
    """ create an mtt client dict plugin """
    return DummyClientPlugin(config, instance_id)

""" workload plugin_id for the mtt dummy plugin """
@uctt_plugin.Factory(type=uctt_plugin.Type.WORKLOAD, plugin_id=UCTT_PLUGIN_ID_DUMMY)
def uctt_plugin_factory_workload_dummy(config:Config, instance_id: str = ''):
    """ create an mtt workload dict plugin """
    return DummyWorkloadPlugin(config, instance_id)

""" SetupTools EntryPoint BootStrapping """

def uctt_bootstrap(config:Config):
    """ UCTT_Dummy bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass

def configerus_bootstrap(config:Config):
    """ UCTT_Dummy configerus bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
