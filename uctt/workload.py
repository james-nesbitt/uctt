import logging

from configerus.config import Config

from .plugin import UCTTPlugin, Type
from .fixtures import Fixtures

logger = logging.getLogger('uctt.workload')

UCTT_PLUGIN_ID_WORKLOAD = Type.WORKLOAD
""" Fast access to the workload type """

UCTT_WORKLOAD_CONFIG_WORKLOADS_LABEL = 'workloads'
""" A centralized configerus load label for multiple workloads """
UCTT_WORKLOAD_CONFIG_WORKLOAD_LABEL = 'workload'
""" A centralized configerus load label for a workload """
UCTT_WORKLOAD_CONFIG_WORKLOADS_KEY = 'workloads'
""" A centralized configerus key for multiple workloads """
UCTT_WORKLOAD_CONFIG_WORKLOAD_KEY = 'workload'
""" A centralized configerus key for one workload """


class WorkloadBase(UCTTPlugin):
    """ Base class for workload plugins """

    def set_fixtures(self, fixtures: Fixtures):
        """ Allow the workload to pull needed fixtures from a Fixtures object

        Raises:
        -------

        Can throw a KeyError if it can't find a needed fixture.

        """
        raise NotImplementedError(
            "This workload plugin has not implemented set_fixtures()")

    def apply(self):
        """ Run the workload

        @NOTE Needs a kubernetes client fixture to run.  Use .set_fixtures() first

        """
        raise NotImplementedError(
            "This workload plugin has not implemented apply()")

    def destroy(self):
        """ destroy any created resources """
        raise NotImplementedError(
            "This workload plugin has not implemented destroy()")
