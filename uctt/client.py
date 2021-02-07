import logging

from configerus.config import Config

from .plugin import UCTTPlugin, Type

logger = logging.getLogger('uctt.client')

UCTT_PLUGIN_ID_CLIENT = Type.CLIENT
""" Fast access to the client plugin_id """


class ClientBase(UCTTPlugin):
    """ Base class for client plugins """

    def arguments(**kwargs):
        """ Receive a list of arguments for this client """
        raise NotImplemented(
            'arguments() was not implemented for this client plugin')
