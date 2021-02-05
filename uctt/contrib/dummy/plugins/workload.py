"""

Dummy workload plugin

"""
from typing import Dict, Any
import logging

import uctt
from uctt.workload import WorkloadBase

logger = logging.getLogger('uctt.contrib.dummy.workload')

class DummyWorkloadPlugin(WorkloadBase):
    """ Dummy workload class """

    def __init__(self, config, instance_id):
        """ Run the super constructor but also set class properties """
        super(WorkloadBase, self).__init__(config, instance_id)

        self.outputs = {}

    def arguments(self, outputs:Dict[str, Any]={}, clients:Dict[str, Any]={}):
        """ Take workload arguments

        Parameters:
        -----------

        outputs (Dict[Dict]) : pass in a dictionary which defines outputs that
            should be returned

        clients (Dict[Dict]) : pass in a dictionary which defines which clients
            should be requested when working on a provisioner

        """
        self.outputs = uctt.new_outputs_from_dict(outputs, self.config)

    def get_output(self, instance_id:str):
        """ Retrieve a dummy output """
        logger.info("{}:execute: get_output()".format(self.instance_id))
        if not self.outputs:
            raise ValueError('No outputs have been added to the dummy workload')
        return self.outputs.get_plugin(instance_id=instance_id)
