"""

Dummy workload plugin

"""
from typing import Dict, Any
import logging

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.workload import WorkloadBase
from uctt.fixtures import UCCTFixturesPlugin

logger = logging.getLogger('uctt.contrib.dummy.workload')

class DummyWorkloadPlugin(WorkloadBase, UCCTFixturesPlugin):
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

        fixtures = environment.add_fixtures_from_dict(plugin_list=fixtures)
        """ All fixtures added to this dummy plugin. """
        UCCTFixturesPlugin.__init__(self, fixtures)
