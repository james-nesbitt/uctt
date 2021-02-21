"""

MTT Terraform

MTT contrib functionality for terraform.  Primarily a terraform provisioner
plugin.

"""
from typing import Any

from configerus.loaded import LOADED_KEY_ROOT

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .provisioner import TerraformProvisionerPlugin, TERRAFORM_PROVISIONER_CONFIG_LABEL

UCTT_TERRAFORM_PROVISIONER_PLUGIN_ID = 'uctt_terraform'
""" Terraform provisioner plugin id """


@Factory(type=Type.PROVISIONER, plugin_id=UCTT_TERRAFORM_PROVISIONER_PLUGIN_ID)
def uctt_plugin_factory_provisioner_terraform(
        environment: Environment, instance_id: str = "", label: str = TERRAFORM_PROVISIONER_CONFIG_LABEL, base: Any = LOADED_KEY_ROOT):
    """ create an mtt provisionersss dict plugin """
    return TerraformProvisionerPlugin(environment, instance_id, label, base)


UCTT_TERRAFORM_CLI_PLUGIN_ID = 'uctt_terraform'
""" cli plugin_id for the info plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_TERRAFORM_CLI_PLUGIN_ID)
def uctt_terraform_factory_cli_terraform(
        environment: Environment, instance_id: str = ''):
    """ create an info cli plugin """
    return TerraformCliPlugin(environment, instance_id)


""" SetupTools EntryPoint UCTT BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT_Terraform bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorator to register our plugin.

    """
    pass
