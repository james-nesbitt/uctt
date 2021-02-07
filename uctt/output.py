import logging

from configerus.config import Config

from .plugin import UCTTPlugin, Type

logger = logging.getLogger('uctt.output')

UCTT_PLUGIN_ID_OUTPUT = Type.OUTPUT
""" Fast access to the output plugin type """


class OutputBase(UCTTPlugin):
    """ Base class for output plugins """
    pass
