"""

Common UCTT plugins

"""
from typing import Dict, Any

from configerus.loaded import LOADED_KEY_ROOT
from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .dict_output import DictOutputPlugin
from .text_output import TextOutputPlugin
from .combo_provisioner import ComboProvisionerPlugin, COMBO_PROVISIONER_CONFIG_LABEL

UCTT_PLUGIN_ID_OUTPUT_DICT = 'dict'
""" output plugin_id for the dict plugin """


@Factory(type=Type.OUTPUT, plugin_id=UCTT_PLUGIN_ID_OUTPUT_DICT)
def uctt_plugin_factory_output_dict(
        environment: Environment, instance_id: str = '', data: Dict = {}, validator: str = ''):
    """ create an output dict plugin """
    return DictOutputPlugin(environment, instance_id, data, validator)


UCTT_PLUGIN_ID_OUTPUT_TEXT = 'text'
""" output plugin_id for the text plugin """


@Factory(type=Type.OUTPUT, plugin_id=UCTT_PLUGIN_ID_OUTPUT_TEXT)
def uctt_plugin_factory_output_text(
        environment: Environment, instance_id: str = '', text: str = ''):
    """ create an output text plugin """
    return TextOutputPlugin(environment, instance_id, text)


UCTT_PLUGIN_ID_PROVISIONER_COMBO = 'combo'
""" provisioner plugin_id for the combo plugin """


@Factory(type=Type.PROVISIONER, plugin_id=UCTT_PLUGIN_ID_PROVISIONER_COMBO)
def uctt_plugin_factory_provisioner_combo(
        environment: Environment, instance_id: str = '', label: str = COMBO_PROVISIONER_CONFIG_LABEL, base: Any = LOADED_KEY_ROOT):
    """ create a provisioner combo plugin """
    return ComboProvisionerPlugin(
        environment, instance_id, label=label, base=base)


""" SetupTools EntryPoint BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT Bootstrapper - don't actually do anything """
    pass
