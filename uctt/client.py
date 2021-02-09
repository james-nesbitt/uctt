import logging

from configerus.config import Config

from .plugin import UCCTArgumentsPlugin, Type

logger = logging.getLogger('uctt.client')

UCTT_PLUGIN_TYPE_CLIENT = Type.CLIENT
""" Fast access to the client plugin_id """

UCTT_OUTPUT_CONFIG_CLIENTS_LABEL = 'clients'
""" A centralized configerus label for multiple clients """
UCTT_OUTPUT_CONFIG_CLIENTS_KEY = 'clients'
""" A centralized configerus key for multiple clients """
UCTT_OUTPUT_CONFIG_CLIENT_KEY = 'client'
""" A centralized configerus key for one client """


class ClientBase(UCCTArgumentsPlugin):
    """ Base class for client plugins """
    pass
