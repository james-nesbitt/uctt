"""

Common UCTT plugins

"""
from typing import Dict

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .dict_output import DictOutputPlugin
from .text_output import TextOutputPlugin

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


""" SetupTools EntryPoint BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT Bootstrapper - don't actually do anything """
    pass
