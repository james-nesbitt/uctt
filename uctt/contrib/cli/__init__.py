"""

UCTT Cli package

"""

import logging

from configerus.config import Config

from uctt.plugin import Type, Factory

from .info import InfoCliPlugin
from .config import ConfigCliPlugin
from .provisioner import ProvisionerCliPlugin

logger = logging.getLogger('uctt.cli')

UCTT_PLUGIN_ID_CLI_INFO = 'info'
""" cli plugin_id for the info plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_PLUGIN_ID_CLI_INFO)
def uctt_plugin_factory_cli_info(config: Config, instance_id: str = ''):
    """ create an info cli plugin """
    return InfoCliPlugin(config, instance_id)


UCTT_PLUGIN_ID_CLI_CONFIG = 'config'
""" cli plugin_id for the config plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_PLUGIN_ID_CLI_CONFIG)
def uctt_plugin_factory_cli_config(config: Config, instance_id: str = ''):
    """ create a config cli plugin """
    return ConfigCliPlugin(config, instance_id)


UCTT_PLUGIN_ID_CLI_PROVISIONER = 'provisioner'
""" cli plugin_id for the provisioner plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_PLUGIN_ID_CLI_PROVISIONER)
def uctt_plugin_factory_provisioner_config(
        config: Config, instance_id: str = ''):
    """ create a provisioner cli plugin """
    return ProvisionerCliPlugin(config, instance_id)


""" SetupTools EntryPoint BootStrapping """


def bootstrap(config: Config):
    """ UCTT Bootstrapper - don't actually do anything """
    pass
