"""

MTT Docker

MTT contrib package for docker functionality, specifically for registering
a Docker client plugin.

"""

import os
from configerus.config import Config

from uctt import plugin as uctt_plugin

from .plugins.client import DockerClientPlugin

UCTT_PLUGIN_ID_DOCKER_CLIENT='mtt_docker'
""" client plugin_id for the mtt dummy plugin """
@uctt_plugin.Factory(type=uctt_plugin.Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_DOCKER_CLIENT)
def uctt_plugin_factory_client_docker(config: Config, instance_id: str = ''):
    """ create an mtt client dict plugin """
    return DockerClientPlugin(config, instance_id)

""" SetupTools EntryPoint BootStrapping """

def uctt_bootstrap(config:Config):
    """ UCTT_Docker bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass

def configerus_bootstrap(config:Config):
    """ UCTT_Docker configerus bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
