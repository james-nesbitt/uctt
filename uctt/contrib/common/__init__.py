"""

Common UCTT plugins

"""
from configerus.config import Config

from uctt import plugin as uctt_plugin

from .dict_output import DictOutputPlugin
from .text_output import TextOutputPlugin

UCTT_PLUGIN_ID_OUTPUT_DICT = 'dict'
""" output plugin_id for the dict plugin """


@uctt_plugin.Factory(type=uctt_plugin.Type.OUTPUT,
                     plugin_id=UCTT_PLUGIN_ID_OUTPUT_DICT)
def uctt_plugin_factory_output_dict(config: Config, instance_id: str = ''):
    """ create an output dict plugin """
    return DictOutputPlugin(config, instance_id)


UCTT_PLUGIN_ID_OUTPUT_TEXT = 'text'
""" output plugin_id for the text plugin """


@uctt_plugin.Factory(type=uctt_plugin.Type.OUTPUT,
                     plugin_id=UCTT_PLUGIN_ID_OUTPUT_TEXT)
def uctt_plugin_factory_output_text(config: Config, instance_id: str = ''):
    """ create an output text plugin """
    return TextOutputPlugin(config, instance_id)


""" SetupTools EntryPoint BootStrapping """


def bootstrap(config: Config):
    """ UCTT Bootstrapper - don't actually do anything """
    pass
