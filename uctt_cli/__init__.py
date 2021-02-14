"""

UCTT Cli package

"""

import logging

from uctt.plugin import Type, Factory
from uctt.environment import Environment

from .info import InfoCliPlugin
from .environment import EnvironmentCliPlugin
from .config import ConfigCliPlugin
from .provisioner import ProvisionerCliPlugin

logger = logging.getLogger('uctt.cli')

UCTT_PLUGIN_ID_CLI_INFO = 'info'
""" cli plugin_id for the info plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_PLUGIN_ID_CLI_INFO)
def uctt_plugin_factory_cli_info(
        environment: Environment, instance_id: str = ''):
    """ create an info cli plugin """
    return InfoCliPlugin(environment, instance_id)


UCTT_PLUGIN_ID_CLI_CONFIG = 'config'
""" cli plugin_id for the config plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_PLUGIN_ID_CLI_CONFIG)
def uctt_plugin_factory_cli_config(
        environment: Environment, instance_id: str = ''):
    """ create a config cli plugin """
    return ConfigCliPlugin(environment, instance_id)


UCTT_PLUGIN_ID_CLI_ENVIRONMENT = 'environment'
""" cli plugin_id for the environment plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_PLUGIN_ID_CLI_ENVIRONMENT)
def uctt_plugin_factory_cli_environment(
        environment: Environment, instance_id: str = ''):
    """ create a config cli plugin """
    return EnvironmentCliPlugin(environment, instance_id)


UCTT_PLUGIN_ID_CLI_PROVISIONER = 'provisioner'
""" cli plugin_id for the provisioner plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_PLUGIN_ID_CLI_PROVISIONER)
def uctt_plugin_factory_provisioner_config(
        environment: Environment, instance_id: str = ''):
    """ create a provisioner cli plugin """
    return ProvisionerCliPlugin(environment, instance_id)


""" SetupTools EntryPoint BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT Bootstrapper - don't actually do anything """
    pass