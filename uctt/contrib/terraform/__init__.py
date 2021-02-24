"""

MTT Terraform

MTT contrib functionality for terraform.  Primarily a terraform provisioner
plugin.

"""
from typing import Any

from configerus.loaded import LOADED_KEY_ROOT
from configerus.contrib.dict import PLUGIN_ID_SOURCE_DICT
from configerus.contrib.jsonschema.validate import PLUGIN_ID_VALIDATE_JSONSCHEMA_SCHEMA_CONFIG_LABEL

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .cli import TerraformCliPlugin
from .provisioner import TerraformProvisionerPlugin, TERRAFORM_PROVISIONER_CONFIG_LABEL, TERRAFORM_VALIDATE_JSONSCHEMA

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

TERRAFORM_VALIDATION_CONFIG_SOURCE_INSTANCE_ID = "terraform_validation"


def bootstrap(environment: Environment):
    """ UCTT_Terraform bootstrap

    What we do here is collect jsonschema for components such as 'provisioner'
    and add it to the environment config as a new source.  Then any code
    interacting with the environment can validate config.

    Parameters:
    -----------

    env (Environment) : an environment which should have validation config added
        to.

    """

    environment.config.add_source(PLUGIN_ID_SOURCE_DICT, TERRAFORM_VALIDATION_CONFIG_SOURCE_INSTANCE_ID, priority=30).set_data({
        PLUGIN_ID_VALIDATE_JSONSCHEMA_SCHEMA_CONFIG_LABEL: {
            TERRAFORM_PROVISIONER_CONFIG_LABEL: TERRAFORM_VALIDATE_JSONSCHEMA
        }
    })
