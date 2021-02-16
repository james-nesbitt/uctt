"""

MTT Dummy

Dummy plugin functionality.  Various plugins that can be used as placeholders
and for testing.

"""

import logging
from typing import Any, Dict

from configerus.loaded import LOADED_KEY_ROOT

from uctt.plugin import Factory, Type
from uctt.environment import Environment
from uctt.provisioner import UCTT_PROVISIONER_CONFIG_PROVISIONER_LABEL

from .provisioner import DummyProvisionerPlugin
from .client import DummyClientPlugin
from .workload import DummyWorkloadPlugin

UCTT_PLUGIN_ID_DUMMY = 'dummy'
""" All of the dummy plugins use 'dummy' as their plugin_id """


@Factory(type=Type.PROVISIONER, plugin_id=UCTT_PLUGIN_ID_DUMMY)
def uctt_plugin_factory_provisioner_dummy(
        environment: Environment, instance_id: str = '', fixtures: Dict[str, Dict[str, Any]] = {}):
    """ create an mtt provisionersss dict plugin """
    return DummyProvisionerPlugin(environment, instance_id, fixtures)


@Factory(type=Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_DUMMY)
def uctt_plugin_factory_client_dummy(
        environment: Environment, instance_id: str = '', fixtures: Dict[str, Dict[str, Any]] = {}):
    """ create an mtt client dict plugin """
    return DummyClientPlugin(environment, instance_id, fixtures)


@Factory(type=Type.WORKLOAD, plugin_id=UCTT_PLUGIN_ID_DUMMY)
def uctt_plugin_factory_workload_dummy(
        environment: Environment, instance_id: str = '', fixtures: Dict[str, Dict[str, Any]] = {}):
    """ create an mtt workload dict plugin """
    return DummyWorkloadPlugin(environment, instance_id, fixtures)


""" SetupTools EntryPoint UCTT BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT_Dummy bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
