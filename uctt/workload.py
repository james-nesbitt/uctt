import logging

from configerus.config import Config

from .plugin import UCTTPlugin, Type

logger = logging.getLogger('uctt.workload')

UCTT_PLUGIN_ID_WORKLOAD = Type.WORKLOAD
""" Fast access to the workload type """


class WorkloadBase(UCTTPlugin):
    """ Base class for workload plugins """

    def arguments(**kwargs):
        """ Receive a list of arguments for this workload """
        raise NotImplemented(
            'arguments() was not implemented for this workload plugin')
