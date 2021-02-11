import logging
from enum import Enum, unique

from configerus.config import Config

logger = logging.getLogger('uctt.plugin')

UCTT_PLUGIN_CONFIG_KEY_PLUGINID = 'plugin_id'
""" configerus .get() key for plugin_id """
UCTT_PLUGIN_CONFIG_KEY_INSTANCEID = 'instance_id'
""" configerus .get() key for plugin_id """
UCTT_PLUGIN_CONFIG_KEY_TYPE = 'type'
""" configerus .get() key for plugin type """
UCTT_PLUGIN_CONFIG_KEY_ARGUMENTS = 'arguments'
""" configerus .get() key for plugin arguments """

UCTT_PLUGIN_CONFIG_KEY_PRIORITY = 'priority'
""" will use this Dict key assign an instance a priority when it is created. """
UCTT_PLUGIN_CONFIG_KEY_CONFIG = 'config'
""" will use this Dict key as additional config """
UCTT_PLUGIN_CONFIG_KEY_VALIDATORS = 'validators'
""" will use this Dict key from the output config to decide what validators to apply to the plugin """


class UCTTPlugin():
    """ Base MTT Plugin which all plugins can extend """

    def __init__(self, config: Config, instance_id: str):
        """
        Parameters:
        -----------

        config (Config) : all plugins receive a config object

        id (str) : instance id for the plugin.

        """
        self.config = config
        self.instance_id = instance_id


class UCCTArgumentsPlugin(UCTTPlugin):
    """ Base class for output plugins that receives arguments """

    def arguments(**kwargs):
        """ Receive a list of arguments for this client """
        raise NotImplemented(
            'arguments() was not implemented for this client plugin')


@unique
class Type(Enum):
    """ Enumerator to match plugin types to plugin labels """
    CLIENT = 'uctt.plugin.client'
    """ Plugins which interact with clusters """
    SOURCE = 'uctt.plugin.configsource'
    """ A Config source handler """
    OUTPUT = 'uctt.plugin.output'
    """ A Config output handler """
    PROVISIONER = 'uctt.plugin.provisioner'
    """ A cluster provisioner plugin """
    WORKLOAD = 'uctt.plugin.workload'
    """ Plugins which use clients/provisioners to apply a workload to a cluster """
    CLI = 'uctt.plugin.cli'
    """ Plugins extend the uctt cli """


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
        logger.debug(
            "Plugin factory registered `%s:%s`",
            type.value,
            plugin_id)
        self.plugin_id = plugin_id
        self.type = type

        if not self.type.value in self.registry:
            self.registry[self.type.value] = {}

    def __call__(self, func):
        """ call the decorated function

        Returns:

        wrapped function(config: Config)
        """
        def wrapper(config: Config, instance_id: str):
            logger.debug(
                "plugin factory exec: %s:%s",
                self.type.value,
                self.plugin_id)
            plugin = func(config=config, instance_id=instance_id)
            if not isinstance(plugin, UCTTPlugin):
                logger.warn(
                    "plugin factory did not return an instance of MTT Plugin `{}:{}`".format(
                        self.type.value, self.plugin_id))

            return plugin

        self.registry[self.type.value][self.plugin_id] = wrapper
        return wrapper

    def create(self, config: Config, instance_id: str):
        """ Get an instance of a plugin as created by the decorated """
        try:
            factory = self.registry[self.type.value][self.plugin_id]
        except KeyError:
            raise NotImplementedError(
                "MTT Plugin instance '{}:{}' has not been registered.".format(
                    self.type.value, self.plugin_id))
        except Exception as e:
            raise Exception(
                "Could not create Plugin instance '{}:{}' as the plugin factory produced an exception".format(
                    self.type.value, self.plugin_id)) from e

        return factory(config=config, instance_id=instance_id)
