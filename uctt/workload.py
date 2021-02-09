import logging

from configerus.config import Config

from .plugin import UCCTArgumentsPlugin, Type

logger = logging.getLogger('uctt.workload')

UCTT_PLUGIN_ID_WORKLOAD = Type.WORKLOAD
""" Fast access to the workload type """

UCTT_OUTPUT_CONFIG_WORKLOADS_LABEL = 'workloads'
""" A centralized configerus load label for multiple workloads """
UCTT_OUTPUT_CONFIG_WORKLOADS_KEY = 'workloads'
""" A centralized configerus key for multiple workloads """
UCTT_OUTPUT_CONFIG_WORKLOAD_KEY = 'workload'
""" A centralized configerus key for one workload """


class WorkloadBase(UCCTArgumentsPlugin):
    """ Base class for workload plugins """
    pass
