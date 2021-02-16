import logging

from configerus.config import Config

from .plugin import UCTTPlugin, Type

logger = logging.getLogger('uctt.output')

UCTT_PLUGIN_TYPE_OUTPUT = Type.OUTPUT
""" Fast access to the output plugin type """

UCTT_OUTPUT_CONFIG_OUTPUTS_LABEL = 'outputs'
""" A centralized configerus load label for multiple outputs """
UCTT_OUTPUT_CONFIG_OUTPUT_LABEL = 'output'
""" A centralized configerus load label for an output """
UCTT_OUTPUT_CONFIG_OUTPUTS_KEY = 'outputs'
""" A centralized configerus key for multiple outputs """
UCTT_OUTPUT_CONFIG_OUTPUT_KEY = 'output'
""" A centralized configerus key for one output """


class OutputBase(UCTTPlugin):
    """ Base class for output plugins """
    pass

    def has_outout(self):
        """ Does this plugin have output """
        raise NotImplemented("this functionality has not yet been written.")
