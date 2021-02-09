"""

Generic Plugin construction

We have a whole module for general plugin creation because we want to keep the
__init__.py as short as possible to focus on exports.

Here we have methods that can create lists/sets of plugins as PluginInstances
objects, or individual plugins.
PluginInstances are used for sets of plugins in order to leverage the searching
features.  Sorting is there but not heavily leveraged.

The primary consumer of this code is the uctt package (__init__.py) where there
are a number of plugin type specific factory methods for general consumption.

Sets and individual plugins can be created from configerus config (preferred) or
python nested dicts.  The dicts are actually just converted to configerus
sources and passed to the config based methods.

We used configerus configs:
1. to gain deep searching when looking for config;
2. to allow for configerus pattern formatting and validation;
3. to standardize.

The process for plugin creation is based on convention of layout of the config
source.

1. we always need a 'type' (UCTT_PLUGIN_CONFIG_KEY_TYPE) to know what type of
    plugin to create.  You can create mixed lists by relying on config to
    describe what type to create;
2. we always want a `plugin_id` (UCTT_PLUGIN_CONFIG_KEY_PLUGINID) to know what
    plugin to create;
3. every plugin needs an `instance_id` (UCTT_PLUGIN_CONFIG_KEY_INSTANCEID if
    you want to be able to retrieve it by name. This can be pulled from the list
    keys, or config, but the individual plugin methods allow it to be specified;
4. plugin `priority` can be specified if you want to add multiple similar plugins
    but prefer one over another on generic retrieval;
5. if creating individual plugins, you can include additional `config` which
    will be made available to the plugin as an additional config source (dict);
6 it is possible to include a configerus validator key which will be applied to
    the config for each plugin before it is created.

"""
import logging
from typing import List, Dict, Any

from configerus.config import Config
from configerus.loaded import LOADED_KEY_ROOT
from configerus.contrib.dict import PLUGIN_ID_SOURCE_DICT

from .plugin import (Factory, Type, UCTTPlugin, UCTT_PLUGIN_CONFIG_KEY_TYPE,
                     UCTT_PLUGIN_CONFIG_KEY_PLUGINID, UCTT_PLUGIN_CONFIG_KEY_INSTANCEID,
                     UCTT_PLUGIN_CONFIG_KEY_ARGUMENTS, UCTT_PLUGIN_CONFIG_KEY_PRIORITY, UCTT_PLUGIN_CONFIG_KEY_CONFIG,
                     UCTT_PLUGIN_CONFIG_KEY_VALIDATORS)
# a lot of centralized config labels and keys are kept in .plugin
from .instances import PluginInstances


""" configerus .get() key for plugin type """
logger = logging.getLogger('uctt.construction')


def new_plugins_from_config(config: Config, label: str, base: Any = LOADED_KEY_ROOT, type: Type = '', validator: str = '',
                            exception_if_missing: bool = False) -> PluginInstances:
    """ Create plugins from some config

    This method will interpret some config values as being usable to build a Dict
    of plugins from.

    Parameters:
    -----------

    config (Config) : Used to load and get the plugin configuration

    label (str) : config label to load to pull plugin configuration. That
        label is loaded and config is pulled to produce a list of plugins

    base (str|List) : config key to get a Dict of plugins configurations.  This
        should point to a dict of plugin configurations.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    type (.plugin.Type) : plugin type to create, pulled from the config/dict if
        omitted

    validator (str) : optionally use a configerus validator on the instance
        config/dict before a plugin is created.

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
    instances = PluginInstances(config=config)
    """ plugin set which will be used to create new plugins """

    try:
        plugin_config = config.load(label)
        plugin_list = plugin_config.get(base, exception_if_missing=True)
    except KeyError as e:
        if exception_if_missing:
            return KeyError('Could not load any config for plugin generation')
            # there is not config so we can ignore this
        else:
            return instances

    # we are going to be pasing key lists to configerus for this instance
    # so make sure that we have the list key type.
    if not isinstance(base, list):
        base = [base]

    for instance_id in plugin_list.keys():
        # configerus loaded .get() key path for the instance
        instance_base = base.copy()
        instance_base.append(instance_id)

        new_plugin_from_config(
            config=config,
            label=label,
            base=instance_base,
            type=type,
            instance_id=instance_id,
            validator=validator,
            instances=instances)

    return instances


def new_plugins_from_dict(config: Config, plugin_list: Dict[str, Dict[str, Any]], type: Type = '',
                          validator: str = '') -> PluginInstances:
    """ Create a set of plugins from Dict information

    The passed dict should be a key=>details map of plugins, which will be turned
    into a PluginInstances map of plugins that can be used to interact with the
    objects.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    type (.plugin.Type) : plugin type to create, pulled from the config/dict if
        omitted

    provisioner_list (Dict[str, Dict]) : map of key=> config dicts, where each dict
        contains all of the information that is needed to build the plugin.

        for details, @see new_plugin_from_dict

    validator (str) : optionally use a configerus validator on the instance
        config/dict before a plugin is created.

    Returns:
    --------

    A PluginsInstances object with the plugin objects created

    """
    instances = PluginInstances(config=config)

    if not isinstance(plugin_list, dict):
        raise ValueError(
            'Did not receive a good dict of config to make plugins from: %s',
            plugin_list)

    for instance_id, plugin_dict in plugin_list.items():
        new_plugin_from_dict(
            config=config,
            plugin_dict=plugin_dict,
            type=type,
            instance_id=instance_id,
            validator=validator,
            instances=instances)

    return instances


def new_plugin_from_config(config: Config, label: str, base: Any = LOADED_KEY_ROOT, type: Type = None,
                           instance_id: str = '', validator: str = '', instances: PluginInstances = None) -> UCTTPlugin:
    """ Create a plugin from some config

    This method will interpret some config values as being usable to build plugin

    Using a configerus config object allows us to leverage advanced configerus
    features such as tree searching, formatting and validation.

    What is looked for:

    1. valdiators if we need to validate the entire label/key before using it
    2. type if we did not receive a type
    3. plugin_id : which will tell us what plugin to load
    4. optional instance_id if none was passed
    5. config if you want config added - ONLY if instances is None
       (plugins in PluginInstances cannot override config objects)
    6. arguments that will be executed on an argument() method if the
        plugin has it.

    Parameters:
    -----------

    config (Config) : Used to load and get the plugin configuration

    type (.plugin.Type) : plugin type to create, pulled from the config/dict if
        omitted

    label (str) : config label to load to pull plugin configuration. That
        label is loaded and config is pulled to produce a list of plugins

    base (str|List) : config key used as a .get() base for all gets.  With this
        you can instruct to pull config from a section of loaded config.
        A list of strings is valid because configerus.loaded.get() can take that
        as an argument. We will be using the list syntax anyway.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements.

    instance_id (str) : optionally pass an instance_id for the item.

    validator (str) : optionally use a configerus validator on the entire .get()
        for the instance config.

    instances (PluginInstances) : if provided, plugins are created by the object
        and added to it, otherwise plugins are created directly

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
    logger.debug('Create plugin [{}][{}]'.format(type, instance_id))

    if not isinstance(base, list):
        base = [base]

    config_plugin = config.load(label)
    """ loaded configuration for the plugin """

    validators = []
    config_validators = config_plugin.get(
        base + [UCTT_PLUGIN_CONFIG_KEY_VALIDATORS])
    if config_validators:
        validators = config_validators
    if validator:
        validators.append(validator)
    if len(validators):
        for validator in validators:
            config_plugin.get(base, validator=validator)

    plugin_id = config_plugin.get(base + [UCTT_PLUGIN_CONFIG_KEY_PLUGINID])
    if not plugin_id:
        raise ValueError(
            "Could not find a plugin_id when trying to create a plugin:[{}][{}][{}] : {}".format(type, label, base, config_plugin.get(base)))

    if type is None:
        type = config_plugin.get(base + [UCTT_PLUGIN_CONFIG_KEY_TYPE])
    if not type:
        raise ValueError(
            "Could not find a plugin type when trying to create a plugin:[{}][{}][{}] : {}".format(type, label, base, config_plugin.get(base)))

    # if no instance_id was passed, try to load one or just make one up
    if not instance_id:
        instance_id = config_plugin.get(
            base + [UCTT_PLUGIN_CONFIG_KEY_INSTANCEID])
        if not instance_id:
            instance_id = '{}-{}'.format(type, plugin_id)

    if instances is None:
        # we are creating a plugin directly

        # If we were given a output config, then create a copy of the config
        # object and add the passed config as new sources to the copy
        plugin_config_dict = config_plugin.get(
            base + [UCTT_PLUGIN_CONFIG_KEY_CONFIG])
        if plugin_config_dict:
            config = config.copy()
            # Add a dict source plugin for the passed 'config', giving it source id
            # just to make identification easier
            config_source_instance_id = 'plugin-{}-{}-{}'.format(
                type, plugin_id, instance_id)
            """ use this for aesthetics, as the new config source instance id """
            config.add_source(
                PLUGIN_ID_SOURCE_DICT,
                config_source_instance_id).set_data(plugin_config_dict)

        # Create the plugin directlu
        plugin = new_plugin(
            config=config,
            type=type,
            plugin_id=plugin_id,
            instance_id=instance_id)
    else:
        # We are creating an instance, so we can look for a priority

        priority = config_plugin.get(
            base + [UCTT_PLUGIN_CONFIG_KEY_INSTANCEID])
        if not priority:
            priority = config.default_priority()
            """ instance priority - this is actually a stupid place to get it from """

        # we can't pass config if creating the plugin as an instance in an instance list
        # as that structure needs tight control over config for copying etc.
        if config_plugin.get(base + [UCTT_PLUGIN_CONFIG_KEY_CONFIG]):
            logger.warn(
                'Creating a plugin for an instance list, but was given config overrides.  Ignoring it as this is not possible.')

        plugin = instances.add_plugin(
            type=type,
            plugin_id=plugin_id,
            instance_id=instance_id,
            priority=priority)

    if hasattr(plugin, 'arguments') and callable(getattr(plugin, 'arguments')):
        plugin_args = config_plugin.get(
            base + [UCTT_PLUGIN_CONFIG_KEY_ARGUMENTS])
        if plugin_args:
            plugin.arguments(**plugin_args)

    return plugin


def new_plugin_from_dict(config: Config, plugin_dict: Dict[str, Any], type: Type = None, instance_id: str = '',
                         validator: str = '', instances: PluginInstances = None) -> UCTTPlugin:
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

    type (.plugin.Type) : plugin type to create, pulled from the config/dict if
        omitted

    client_dict (Dict[str,Any]) : Dict from which all needed information will
        be pulled.  Optionally additional config sources can be included as well
        as arguments which could be passed to the plugin.

        @see new_plugin_from_dict for more details.

    instance_id (str) : optionally pass an instance_id for the item.

    validator (str) : optionally use a configerus validator on the entire .get()
        for the instance config.

    instances (PluginInstances) : if provided, plugins are created by the object
        and added to it, otherwise plugins are created directly

    Return:
    -------

    A plugin object (UCTTPlugin)

    """
    plugin_config_source_id = '{}-{}-plugin_dict'.format(type, instance_id)
    """ unique identifier for this dict as a config label """

    instance_config = config.copy()
    instance_config.add_source(
        PLUGIN_ID_SOURCE_DICT, ).set_data({
            plugin_config_source_id: plugin_dict
        })
    return new_plugin_from_config(config=instance_config, type=type, label=plugin_config_source_id,
                                  base=LOADED_KEY_ROOT, instance_id=instance_id, validator=validator, instances=instances)


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
