import functools
import logging
from enum import Enum, unique

from configerus.config import Config

logger = logging.getLogger('uctt.plugin')

class MTTPlugin():
    """ Base MTT Plugin which all plugins can extend """

    def __init__(self, config, instance_id: str):
        """
        Parameters:
        -----------

        config (Config) : all plugins receive a config object

        id (str) : instance id for the plugin.

        """
        self.config = config
        self.instance_id = instance_id

@unique
class Type(Enum):
    """ Enumerator to match plugin types to plugin labels """
    CLIENT        = "mirantis.testing.toolbox.plugin.client"
    """ Plugins which interact with clusters """
    CONFIGSOURCE  = "mirantis.testing.toolbox.plugin.configsource"
    """ A Config source handler """
    OUTPUT  = "mirantis.testing.toolbox.plugin.output"
    """ A Config output handler """
    PROVISIONER   = "mirantis.testing.toolbox.plugin.provisioner"
    """ A cluster provisioner plugin """
    WORKLOAD      = "mirantis.testing.toolbox.plugin.workload"
    """ Plugins which use clients/provisioners to apply a workload to a cluster """

class Factory():
    """ Python decorator class for MTT Plugin factories

    This class should be used to decorate any function which is meant to be a
    factory for MTT plugins.

    If you are writing a plugin factory, decorate it with this class, provide
    the factory type and id values, and then the factory will be avaialble to
    other code.

    If you are trying to get an instance of a plugin, then create an instance of
    this class and use the create() method

    """

    registry = {}
    """ A list of all of the registered factory functions """

    def __init__(self, type: Type, plugin_id: str):
        """ register the decoration """
        logger.debug("Plugin factory registered `%s:%s`", type.value, plugin_id)
        self.plugin_id = plugin_id
        self.type = type

        if not self.type.value in self.registry:
            self.registry[self.type.value] = {}

    def __call__(self, func):
        """ call the decorated function

        Returns:

        wrapped function(config: Config)
        """
        def wrapper(config:Config, instance_id: str):
            logger.debug("plugin factory exec: %s:%s", self.type.value, self.plugin_id)
            plugin = func(config=config, instance_id=instance_id)
            if not isinstance(plugin, MTTPlugin):
                logger.warn("plugin factory did not return an instance of MTT Plugin `{}:{}`".format(self.type.value, self.plugin_id))

            return plugin

        self.registry[self.type.value][self.plugin_id] = wrapper
        return wrapper

    def create(self, config:Config, instance_id: str):
        """ Get an instance of a plugin as created by the decorated """
        try:
            factory = self.registry[self.type.value][self.plugin_id]
        except KeyError:
            raise NotImplementedError("MTT Plugin instance '{}:{}' has not been registered.".format(self.type.value, self.plugin_id))
        except Exception as e:
            raise Exception("Could not create Plugin instance '{}:{}' as the plugin factory produced an exception".format(self.type.value, self.plugin_id)) from e

        return factory(config=config, instance_id=instance_id)


class PluginInstances:
    """ List of plugins wrapped in the PluginInstance struct so that it can be
        prioritized and managed.
    """

    def __init__(self, config):
        self.instances = []
        """ keep a list of all of the plugins as PluginInstance wrappers

            This mixes plugin types together but but it simplifies management
            and storage of plugins """

        self.config = config
        """ A config object is needed for the plugin factories, and it doesn't
            often make sense to use a different config for different plugins """

    def add_plugin(self, type:Type, plugin_id:str, instance_id:str, priority:int, config:Config=None):
        """ Create a configerus plugin and add it to the config object

        Parameters:
        -----------
        type (Type) : instance of the plugin Type enum

        plugin_id (str) : id of the plugin as registered using the plugin
            factory decorater. This has to match a plugin's registration with

        instance_id (str) : Optionally give a plugin instance a name, which it
            might use for internal functionality.
            The "path" source plugin allows string template substitution of the
            "__paths__:instance_id" for the path.

        priority (int) : plugin priority. Use this to set this plugins as
            higher or lower priority than others.

        config (Config) : optional alternative config for creating the plugin

        Returns:
        --------

        Returns the plugin so that you can do any actions to the plugin that it
        supports, and the code here doesn't need to get fancy with function
        arguments

        """
        if not plugin_id:
            raise KeyError("Could not create a plugin as an invalid plugin_id was given: '{}'".format(plugin_id))

        if not type:
            raise KeyError("Could not create a plugin as an invalid type was given: '{}'".format(plugin_id))

        if not instance_id:
            # generate some kind of unique instance_id key
            base_instance_id = "{}_{}".format(type.value, plugin_id)
            index = 1
            instance_id = "{}_{}".format(base_instance_id, index)
            while self.has_plugin(instance_id):
                index = 1
                instance_id = "{}_{}".format(base_instance_id, index)

        if self.has_plugin(instance_id, plugin_id):
            self.warn("Replacing '{}.{}' with new plugin instance".format(plugin_id, instance_id))

        try:
            fac = Factory(type, plugin_id)
            plugin = fac.create(self.config, instance_id)
            instance = PluginInstance(type, plugin_id, instance_id, priority, plugin)

        except NotImplementedError as e:
            raise NotImplementedError("Could not create configerus plugin '{}:{}' as that plugin_id could not be found.".format(type.value, plugin_id)) from e

        self.instances.append(instance)
        return plugin

    """ Accessing plugins """

    def __getitem__(self, instance_id):
        """ For subscriptions assume that an instance_id is being retrieved """
        return self.get_plugin(instance_id=instance_id)

    def get_plugin(self, plugin_id:str='', instance_id:str='', type:Type=None, exception_if_missing: bool=True):
        """ Retrieve a plugin from its instance_id, optionally of a specific type """
        if not (plugin_id or instance_id or type):
            raise Exception("To get a plugin you must for at least one of plugin_id, instance_id or type")

        for plugin_instance in self.instances:
            if plugin_id and not plugin_instance.plugin_id == plugin_id:
                continue
            elif instance_id and not plugin_instance.instance_id==instance_id:
                continue
            elif type and not type==plugin_instance.type:
                continue

            return plugin_instance.plugin
        if exception_if_missing:
            raise KeyError("Could not find plugin {}".format(instance_id if type is None else "{}:{}".format(type.value, instance_id)))
        return False

    def has_plugin(self, plugin_id:str='', instance_id:str='', type:Type=None):
        """ Discover if a plugin had been added with an instance_id, optionally
            of a specific type """
        return bool(self.get_plugin(plugin_id, instance_id, type, exception_if_missing=False))

    def get_ordered_plugins(self, type:Type=None):
        """ order plugin, optionally just one type, by their top down priority

        we process the plugins in three steps:
        1. Optionally filter for type
        2. sort based on priority
        3. collect just the instance plugin objects

        """
        typed_instances = [instance for instance in self.instances if (type is None or instance.type==type)]
        sorted_instances = sorted(typed_instances, key=lambda instance: instance.priority)
        sorted_instances.reverse()
        return [instance.plugin for instance in sorted_instances]

class PluginInstance:
    """ a struct for a plugin instance that also keeps metadata about the instance """

    def __init__(self, type:Type, plugin_id:str, instance_id:str, priority:int, plugin):
        self.type = type
        self.plugin_id = plugin_id
        self.instance_id = instance_id
        self.priority = priority
        self.plugin = plugin
