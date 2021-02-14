"""

Dummy workload plugin

"""
from typing import Dict, Any
import logging

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.workload import WorkloadBase

from .base import DummyFixtures

logger = logging.getLogger('uctt.contrib.dummy.workload')

class DummyWorkloadPlugin(DummyFixtures, WorkloadBase):
    """ Dummy workload class """

    def __init__(self, environment: Environment, instance_id: str, fixtures: Dict[str, Dict[str, Any]] = {}):
        """ Run the super constructor but also set class properties

        Parameters:
        -----------

        outputs (Dict[Dict]) : pass in a dictionary which defines outputs that
            should be returned

        clients (Dict[Dict]) : pass in a dictionary which defines which clients
            should be requested when working on a provisioner

        """
        WorkloadBase.__init__(self, environment, instance_id)
        DummyFixtures.__init__(self, environment, fixtures)
