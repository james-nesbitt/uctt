"""

Dummy client plugin

"""

import logging
from typing import Dict, Any

import uctt
from uctt.client import ClientBase

logger = logging.getLogger('uctt.contrib.dummy.client')

class DummyClientPlugin(ClientBase):
    """ Dummy client class

    As with all dummies, this is a failsafe plugin, that should never throw any
    exceptions if used according to mtt standards.

    It can be used as a placeholder during development, or it can be used to
    log client events and output for greater development and debugging.

    The client will log any method call, including unknown methods, and so it
    can be used in place of any client, if you don't need the methods to return
    anything
    """

    def __init__(self, config, instance_id):
        """ Run the super constructor but also set class properties """
        super(ClientBase, self).__init__(config, instance_id)

        self.outputs = {}

    def arguments(self, outputs:Dict[str, Any]={}):
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
            raise ValueError('No outputs have been added to the dummy client')
        return self.outputs.get_plugin(instance_id=instance_id)
