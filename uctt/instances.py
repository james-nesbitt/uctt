import logging
import copy
from enum import Enum, unique

from configerus.config import Config
from configerus.instances import PluginInstances as configerus_PluginInstances

from .plugin import Factory, Type

logger = logging.getLogger('uctt.plugin')

PLUGIN_DEFAULT_PRIORITY = 75
""" Default plugin priority, which should be a common unprioritized value """


class PluginInstances(configerus_PluginInstances):
    """ List of plugins wrapped in the PluginInstance struct so that it can be
        prioritized and managed.

        This just extends the configerus PluginInstances which already has most
        of what we need.
    """

    def __init__(self, config: Config):
        """

        Set up a configerus PluginInstances set with a built in plugin factory
        and copier.

        Parameters:
        -----------

        config (Config) : config object used to build plugins with.

        """
        super(PluginInstances, self).__init__(self.make_plugin)

        self.config = config

    def copy(selfr):
        """ Make a copy of this plugin list.

        This copies the instance list and by copying every plugin, overriding
        its config and adding it to the new list

        Returns:
        --------

        A copy of this InstanceList, with copies of all of the PluginInstance
        instances with copies of the plugins.
        Changing/Using the copy should not affect the original.

        """
        return super(PluginInstances, self).copy(
            self, self.make_plugin, self.copy_plugin)

    def make_plugin(self, type: Type, plugin_id: str,
                    instance_id: str, priority: int = PLUGIN_DEFAULT_PRIORITY):
        """ Make a new plugin from plugin metadata """
        fac = Factory(type, plugin_id)
        return fac.create(self.config, instance_id)

    def copy_plugin(self, plugin: object):
        """ Make a plugin object """
        plugin_copy = copy.deepcopy(plugin)
        plugin_copy.config = self.config
        return plugin_copy
