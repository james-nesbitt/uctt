"""

Generic Plugin construction

"""
import logging
from typing import List, Dict, Any

from configerus.config import Config
from configerus.loaded import LOADED_KEY_ROOT

from .plugin import Factory, Type, UCTTPlugin
from .instances import PluginInstances

logger = logging.getLogger('uctt.construction')


UCTT_PLUGIN_CONFIG_KEY_PLUGINID = 'plugin_id'
""" plugins_from_config will use this Dict key from the plugin config to decide what plugin to create """
UCTT_PLUGIN_CONFIG_KEY_INSTANCEID = 'instance_id'
""" plugins_from_config will use this Dict key assign an instance_id """
UCTT_PLUGIN_CONFIG_KEY_CONFIG = 'config'
""" new_plugins_from_config will use this Dict key as additional config """
UCTT_PLUGIN_CONFIG_KEY_ARGS = 'arguments'
""" new_plugins_from_config will use this Dict key from the plugin config to decide what arguments to pass to the plugin """


def new_plugins_from_config(
        config: Config, type: Type, label: str, key: str) -> PluginInstances:
    """ Create plugins from some config

    This method will interpret some config values as being usable to build a Dict
    of plugins from.

    Parameters:
    -----------

    config (Config) : Used to load and get the plugin configuration

    label (str) : config label to load to pull plugin configuration. That
        label is loaded and config is pulled to produce a list of plugins

    key (str) : config key to get a Dict of plugins configurations.

    Returns:
    --------

    PluginInstances of your type

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """

    try:
        plugin_config = config.load(label)
        plugin_list = plugin_config.get(key, exception_if_missing=True)
    except KeyError as e:
        # there is not config so we can ignore this
        return {}

    return new_plugins_from_dict(
        config=config, type=type, plugin_list=plugin_list)



def new_plugins_from_dict(config: Config, type: Type,
                          plugin_list: Dict[str, Dict[str, Any]]) -> PluginInstances:
    """ Create a set of plugins from Dict information

    The passed dict should be a key=>details map of plugins, which will be turned
    into a PluginInstances map of plugins that can be used to interact with the
    objects.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    type (.plugin.Type) : plugin type to create

    provisioner_list (Dict[str, Dict]) : map of key=> config dicts, where each dict
        contains all of the information that is needed to build the plugin.

        for details, @see new_plugin_from_dict

    Returns:
    --------

    A PluginsInstances object with the plugin objects created

    """
    plugins = PluginInstances(config=config)

    if not isinstance(plugin_list, dict):
        raise ValueError(
            'Did not receive a good dict of config to make plugins from: %s',
            plugin_list)

    for instance_id, plugin_config in plugin_list.items():
        if not isinstance(plugin_config, dict):
            raise ValueError(
                "Recevied bad plugin configuration, expected Dict[str,Any], got '{}'".format(plugin_config))

        if not UCTT_PLUGIN_CONFIG_KEY_PLUGINID in plugin_config:
            raise ValueError(
                "Plugin dict was missing plugin_id : {}".format(plugin_config))
        plugin_id = plugin_config[UCTT_PLUGIN_CONFIG_KEY_PLUGINID]

        instance_config = config
        # If we were given plugin config, then create a copy of the config
        # object and add the passed config as new sources to the copy
        if UCTT_PLUGIN_CONFIG_KEY_CONFIG in plugin_config:
            instance_config = config.copy()
            instance_config.add_source(
                PLUGIN_ID_SOURCE_DICT,
                'plugin-{}'.format(plugin_id)).set_data(
                plugin_config[UCTT_PLUGIN_CONFIG_KEY_CONFIG])

        # tell the instancelist to build a new plugin
        plugin = plugins.add_plugin(
            type, plugin_id, instance_id, 60)
        if not plugin:
            raise Exception("Did not create a good plugin")

        if UCTT_PLUGIN_CONFIG_KEY_ARGS in plugin_config:
            try:
                arguments = plugin_config[UCTT_PLUGIN_CONFIG_KEY_ARGS]
                plugin.arguments(**arguments)
            except KeyError as e:
                raise Exception(
                    "Plugin [{}] did not like the arguments given: {}".format(
                        plugin, e)) from e

    return plugins


UCTT_PLUGIN_CONFIG_KEY_PLUGINID = 'plugin_id'
""" outputs_from_config will use this Dict key from the output config to decide what plugin to create """
UCTT_PLUGIN_CONFIG_KEY_INSTANCEID = 'instance_id'
""" outputs_from_config will use this Dict key assign an instance_id """
UCTT_PLUGIN_CONFIG_KEY_CONFIG = 'config'
""" new_outputs_from_config will use this Dict key as additional config """
UCTT_PLUGIN_CONFIG_KEY_ARGS = 'arguments'
""" new_outputs_from_config will use this Dict key from the output config to decide what arguments to pass to the plugin """


def new_plugin_from_config(config: Config, type: Type,
                           label: str, key: str, instance_id: str = '') -> UCTTPlugin:
    """ Create a plugin from some config

    This method will interpret some config values as being usable to build plugin

    Using a configerus config object allows us to leverage advanced configerus
    features such as tree searching, formatting and validation.

    Parameters:
    -----------

    config (Config) : Used to load and get the plugin configuration

    type (.plugin.Type) : plugin type to create

    label (str) : config label to load to pull plugin configuration. That
        label is loaded and config is pulled to produce a list of plugins

    key (str) : config key to get a Dict of plugins configurations.

    instance_id (str) : optionally pass an instance_id for the item.

    Returns:
    --------

    PluginInstances of your type

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    config_plugin = config.load(label)
    """ loaded configuration for the plugin """

    plugin_id = config_plugin.get(UCTT_PLUGIN_CONFIG_KEY_PLUGINID)
    if not plugin_id:
        raise ValueError('Could not find a plugin_id when trying to create a plugin')
    # if no instance_id was passed, try to load one or just make one up
    if not instance_id:
        instance_id = config_plugin.get(UCTT_PLUGIN_CONFIG_KEY_INSTANCEID)
    if not instance_id:
        instance_id = '{}-{}'.format(type, plugin_id)

    # If we were given a output config, then create a copy of the config
    # object and add the passed config as new sources to the copy
    plugin_dict = config_plugin.get(UCTT_PLUGIN_CONFIG_KEY_CONFIG)
    if plugin_dict:
        config = config.copy()
        # Add a dict source plugin for the passed 'config', giving it source id
        # just to make identification easier
        instance_config.add_source(
            PLUGIN_ID_SOURCE_DICT, '{}-{}-{}'.format(
                type, plugin_id, instance_id)).set_data(
            plugin_dict[UCTT_PLUGIN_CONFIG_KEY_CONFIG])

    plugin = new_plugin(
        config=config,
        type=type,
        plugin_id=plugin_id,
        instance_id=instance_id)

    plugin_args = config_plugin.get(UCTT_PLUGIN_CONFIG_KEY_ARGS)
    if plugin_args:
        plugin.arguments(**plugin_args)

    return plugin

def new_plugin_from_dict(config: Config, type: Type,
                         plugin_dict: Dict[str, Any], instance_id: str = '') -> UCTTPlugin:
    """ Create a single plugin from a Dict of information for it

    Create a new plugin from a map/dict of settings for the needed parameters.
    To process this, we convert the dict to a configerus dict source, and build
    a plugin using new_plugin_from_config, telling it to read from the added
    config source.

    we use LOADED_KEY_ROOT to tell new_plugin_from_config to load the entire
    configerus source as the definition of the plugin.

    We use a configerus source so that we can get the configerus fancy features
    such as tree searching, formatting and validation.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    type (.plugin.Type) : plugin type to create

    client_dict (Dict[str,Any]) : Dict from which all needed information will
        be pulled.  Optionally additional config sources can be included as well
        as arguments which could be passed to the plugin.

        @see new_plugin_from_dict for more details.

    instance_id (str) : optionally pass an instance_id for the item.

    Return:
    -------

    A plugin object (UCTTPlugin)

    """
    dict_id = '{}-{}-{}-plugin_dict'.format(type, plugin_id, instance_id)
    """ unique identifier for this dict as a config label """

    config = config.copy()
    instance_config.add_source(
        PLUGIN_ID_SOURCE_DICT, ).set_data({
            dict_id: plugin_dict
        })
    return new_plugin_from_config(config, type, dict_id, LOADED_KEY_ROOT, instance_id)


def new_plugin(config: Config, type: Type, plugin_id: str,
               instance_id: str) -> UCTTPlugin:
    """ Create a new plugin from parameters

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    type (.plugin.Type) : plugin type to create

    plugin_id (str) : UCTT plugin id for the plugin type, to tell us what plugin
        factory to load.

        @see .plugin.Factory for more details on how plugins are loaded.

    instance_id (str) : string instance id that will be passed to the new plugin
        object.

    Return:
    -------

    A plugin object (ProvisionerBase)

    """
    fac = Factory(type, plugin_id)
    return fac.create(config, instance_id)
