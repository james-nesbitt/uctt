"""

Ansible provisioner

"""

from typing import Any

from configerus.loaded import LOADED_KEY_ROOT

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .provisioner import AnsibleProvisionerPlugin, ANSIBLE_PROVISIONER_CONFIG_LABEL
from .cli import AnsibleCliPlugin

UCTT_ANSIBLE_PROVISIONER_PLUGIN_ID = 'uctt_ansible'
""" Ansible provisioner plugin id """


@Factory(type=Type.PROVISIONER, plugin_id=UCTT_ANSIBLE_PROVISIONER_PLUGIN_ID)
def uctt_plugin_factory_provisioner_ansible(
        environment: Environment, instance_id: str = "", label: str = ANSIBLE_PROVISIONER_CONFIG_LABEL, base: Any = LOADED_KEY_ROOT):
    """ create an mtt provisionersss dict plugin """
    return AnsibleProvisionerPlugin(environment, instance_id, label, base)


UCTT_ANSIBLE_CLI_PLUGIN_ID = 'uctt_ansible'
""" cli plugin_id for the info plugin """


@Factory(type=Type.CLI, plugin_id=UCTT_ANSIBLE_CLI_PLUGIN_ID)
def uctt_ansible_factory_cli_ansible(
        environment: Environment, instance_id: str = ''):
    """ create an info cli plugin """
    return AnsibleCliPlugin(environment, instance_id)


""" SetupTools EntryPoint UCTT BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT_Ansible bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorator to register our plugin.

    """
    pass
