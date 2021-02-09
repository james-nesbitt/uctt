"""

UCTT Core toolset

In this module, the root package, are found a number of tool plugin constructors
that can be used to get instances of the plugins based on either passed in data
or configerus config.

The contstruction.py module does the heavy lifting of building plugins and
PluginInstances sets.

"""

from importlib import metadata
from typing import Dict, List, Any
import logging

from configerus.config import Config
from configerus.loaded import LOADED_KEY_ROOT

from .plugin import Type
from .instances import PluginInstances
from .constructors import new_plugins_from_config, new_plugins_from_dict, new_plugin_from_config, new_plugin_from_dict, new_plugin
from .provisioner import (
    ProvisionerBase,
    UCTT_PROVISIONER_CONFIG_PROVISIONERS_LABEL,
    UCTT_PROVISIONER_CONFIG_PROVISIONER_LABEL)
from .client import (
    ClientBase,
    UCTT_CLIENT_CONFIG_CLIENTS_LABEL,
    UCTT_CLIENT_CONFIG_CLIENT_LABEL)
from .output import (
    OutputBase,
    UCTT_OUTPUT_CONFIG_OUTPUTS_LABEL,
    UCTT_OUTPUT_CONFIG_OUTPUT_LABEL)
from .workload import (
    WorkloadBase,
    UCTT_WORKLOAD_CONFIG_WORKLOADS_LABEL,
    UCTT_WORKLOAD_CONFIG_WORKLOAD_LABEL)

# make sure that the common factory decorators are run
import uctt.contrib.common

logger = logging.getLogger('uctt')

""" BOOTSTRAPPING """

UCTT_BOOTSTRAP_ENTRYPOINT = 'uctt.bootstrap'
""" SetupTools entry_point used for UCTT bootstrap """


def bootstrap(config: Config, bootstraps=[]):
    """ BootStrap some UCTT distributions

    UCTT bootstrapping is an attempt to allow an easy in to including contrib
    functionality without having to do a lot of Python imports.

    BootStrapping is a setuptools enabled process, where any python package can
    declare a bootstraper, and this function will run that bootstrapper on
    request.
    The BootStrap entry_points are expected to receive a config object on which
    they can operate to add any specific or global functionality.

    BootStraps are typically used for two behaviours:

    1. just import files which run configerus or uctt decorators to register
        plugins
    2. add source/formatter/validator plugins to the passed config object.

    Parameters:
    -----------

    config (configerus.Config) : a config object which bootstrapers can modify.

    bootstrap (List[str]) : a list of string bootstrapper entry_points for the
        ucct.bootstrap entry_points (part of setuptools.)
        Each value needs to refer to a valid entrypoint which will be executed
        with the config object as an argument.

    Returns:
    --------

    The passed in config is returned, but it may be replaced if a bootstrapper
    returns a different object.

    Raises:
    -------

    Raises a KeyError in cases of a bootstrap ID that cannot be found.

    Bootstrappers themselves may raise an exception.

    """
    for bootstrap_id in bootstraps:
        logger.info("Running uctt bootstrap entrypoint: %s", bootstrap_id)
        eps = metadata.entry_points()[UCTT_BOOTSTRAP_ENTRYPOINT]
        for ep in eps:
            if ep.name == bootstrap_id:
                plugin = ep.load()
                plugin(config)
                break
        else:
            raise KeyError(
                "Bootstrap not found {}:{}".format(
                    UCTT_BOOTSTRAP_ENTRYPOINT,
                    bootstrap_id))


""" PROVISIONER CONSTRUCTION """


def new_provisioners_from_config(config: Config,
                                 label: str = UCTT_PROVISIONER_CONFIG_PROVISIONERS_LABEL,
                                 base: Any = LOADED_KEY_ROOT) -> PluginInstances:
    """ Create provisioners from some config

    This method will interpret some config values as being usable to build
    a PluginInstances set of provisioner plugins

    @TODO - we should enable configerus validation

    Parameters:
    -----------

    config (Config) : Used to load and get the provisioner configuration

    label (str) : config label to load to pull provisioner configuration. That
        label is loaded and config is pulled to produce a list of provisioners

    base (str|List) : config key to get a Dict of plugins configurations.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    Returns:
    --------

    PluginInstances of provisioner plugins

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugins_from_config(
        config=config, type=Type.PROVISIONER, label=label, base=base)


def new_provisioner_from_config(config: Config, label: str = UCTT_PROVISIONER_CONFIG_PROVISIONER_LABEL,
                                base: Any = LOADED_KEY_ROOT, instance_id: str = '') -> ProvisionerBase:
    """ Create a provisioner from some config

    This method will interpret some config values as being usable to build a
    provisioner

    Parameters:
    -----------

    config (Config) : Used to load and get the provisioner configuration

    label (str) : config label to load to pull provisioner configuration. That
        label is loaded and config is pulled to produce a list of provisioners

    base (str|List) : config key to get a Dict of plugin configuration.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    instance_id (str) : optionally force a particular instance_id to be assigned

    Returns:
    --------

    provisioner plugin (ProvisionerBase)

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    logger.debug(
        "Creating provisioner: [{}]:[{}][{}]".format(
            label, base, instance_id))
    return new_plugin_from_config(
        config=config, type=Type.PROVISIONER, label=label, base=base)


def new_provisioners_from_dict(
        config: Config, provisioner_list: Dict[str, Dict]) -> PluginInstances:
    """ Create a set of provisioner plugins from Dict information

    The passed dict should be a key=>details map of provisioners, which will be turned
    into a PluginInstances map of plugins that can be used to interact with the
    objects.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    provisioner_list (Dict[str, Dict]) : map of key=> config dicts, where each dict
        contains all of the information that is needed to build the plugin.

        for details, @see new_plugins_from_dict

    Returns:
    --------

    A PluginsInstances object with the plugin objects created

    """
    return new_plugins_from_dict(
        config=config, type=Type.PROVISIONER, plugin_list=provisioner_list)


def new_provisioner_from_dict(
        config: Config, provisioner_dict: Dict[str, Any], instance_id: str = '') -> ProvisionerBase:
    """ Create a provisioner plugin from a Dict of information for it

    Create a new provisioner plugin from a map/dict of settings for the needed parameters.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    provisioner_dict (Dict[str,Any]) : Dict from which all needed information will
        be pulled.  Optionally additional config sources can be included as well
        as arguments which could be passed to the plugin.

        @see new_plugin_from_dict for more details.

    instance_id (str) : optionally force a particular instance_id to be assigned

    Return:
    -------

    A plugin object (ProvisionerBase)

    """
    return new_plugin_from_dict(
        config=config, type=Type.PROVISIONER, plugin_dict=provisioner_dict, instance_id=instance_id)


def new_provisioner(config: Config, plugin_id: str,
                    instance_id: str) -> ProvisionerBase:
    """ Create a new provisioner from parameters

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    plugin_id (str) : UCTT plugin id for the provisioner type, to tell us what plugin
        factory to load.

        @see .plugin.Factory for more details on how plugins are loaded.

    instance_id (str) : string instance id that will be passed to the new plugin
        object.

    Return:
    -------

    A plugin object (ProvisionerBase)

    """
    return new_plugin(config=config, type=Type.PROVISIONER,
                      plugin_id=plugin_id, instance_id=instance_id)


""" CLIENT CONSTRUCTION """


def new_clients_from_config(config: Config,
                            label: str = UCTT_CLIENT_CONFIG_CLIENTS_LABEL,
                            base: Any = LOADED_KEY_ROOT) -> PluginInstances:
    """ Create clients from some config

    This method will interpret some config values as being usable to build
    a PluginInstances set of client plugins

    Parameters:
    -----------

    config (Config) : Used to load and get the client configuration

    label (str) : config label to load to pull client configuration. That
        label is loaded and config is pulled to produce a list of clients

    base (str|List) : config key to get a Dict of plugins configurations.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    Returns:
    --------

    PluginInstances of client plugins

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugins_from_config(
        config=config, type=Type.CLIENT, label=label, base=base)


def new_client_from_config(config: Config,
                           label: str = UCTT_CLIENT_CONFIG_CLIENT_LABEL,
                           base: Any = LOADED_KEY_ROOT) -> ClientBase:
    """ Create a client from some config

    This method will interpret some config values as being usable to build a
    client

    Parameters:
    -----------

    config (Config) : Used to load and get the client configuration

    label (str) : config label to load to pull client configuration. That
        label is loaded and config is pulled to produce a list of clients

    base (str|List) : config key to get a Dict of plugin configuration.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    Returns:
    --------

    client plugin (ClientBase)

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugin_from_config(
        config=config, type=Type.CLIENT, label=label, base=base)


def new_clients_from_dict(
        config: Config, client_list: Dict[str, Dict]) -> PluginInstances:
    """ Create a set of client plugins from Dict information

    The passed dict should be a key=>details map of clients, which will be turned
    into a PluginInstances map of plugins that can be used to interact with the
    objects.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    client_list (Dict[str, Dict]) : map of key=> config dicts, where each dict
        contains all of the information that is needed to build the plugin.

        for details, @see new_plugins_from_dict

    Returns:
    --------

    A PluginsInstances object with the plugin objects created

    """
    return new_plugins_from_dict(
        config=config, type=Type.CLIENT, plugin_list=client_list)


def new_client_from_dict(
        config: Config, client_dict: Dict[str, Any]) -> ClientBase:
    """ Create a single client plugin from a Dict of information for it

    Create a new client plugin from a map/dict of settings for the needed parameters.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    client_dict (Dict[str,Any]) : Dict from which all needed information will
        be pulled.  Optionally additional config sources can be included as well
        as arguments which could be passed to the plugin.

        @see new_plugin_from_dict for more details.

    Return:
    -------

    A plugin object (ClientBase)

    """
    return new_plugin_from_dict(
        config=config, type=Type.CLIENT, plugin_dict=client_dict)


def new_client(config: Config, plugin_id: str, instance_id: str) -> ClientBase:
    """ Create a new client from parameters

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    plugin_id (str) : UCTT plugin id for the client type, to tell us what plugin
        factory to load.

        @see .plugin.Factory for more details on how plugins are loaded.

    instance_id (str) : string instance id that will be passed to the new plugin
        object.

    Return:
    -------

    A plugin object (ClientBase)

    """
    return new_plugin(config=config, type=Type.CLIENT,
                      plugin_id=plugin_id, instance_id=instance_id)


""" OUTPUT CONSTRUCTION """


def new_outputs_from_config(config: Config,
                            label: str = UCTT_OUTPUT_CONFIG_OUTPUTS_LABEL,
                            base: Any = LOADED_KEY_ROOT) -> PluginInstances:
    """ Create outputs from some config

    This method will interpret some config values as being usable to build
    a PluginInstances set of output plugins

    Parameters:
    -----------

    config (Config) : Used to load and get the output configuration

    label (str) : config label to load to pull output configuration. That
        label is loaded and config is pulled to produce a list of outputs

    base (str|List) : config key to get a Dict of plugins configurations.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    Returns:
    --------

    PluginInstances of output plugins

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugins_from_config(
        config=config, type=Type.OUTPUT, label=label, base=base)


def new_output_from_config(config: Config,
                           label: str = UCTT_OUTPUT_CONFIG_OUTPUT_LABEL,
                           base: Any = LOADED_KEY_ROOT) -> OutputBase:
    """ Create a output from some config

    This method will interpret some config values as being usable to build
    output

    Parameters:
    -----------

    config (Config) : Used to load and get the output configuration

    label (str) : config label to load to pull output configuration. That
        label is loaded and config is pulled to produce a list of outputs

    base (str|List) : config key to get a Dict of plugins configurations.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    Returns:
    --------

    output plugin (OutputBase)

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugin_from_config(
        config=config, type=Type.OUTPUT, label=label, base=base)


def new_outputs_from_dict(
        config: Config, output_list: Dict[str, Dict]) -> PluginInstances:
    """ Create a set of output plugins from Dict information

    The passed dict should be a key=>details map of outputs, which will be turned
    into a PluginInstances map of plugins that can be used to interact with the
    objects.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    output_list (Dict[str, Dict]) : map of key=> config dicts, where each dict
        contains all of the information that is needed to build the plugin.

        for details, @see new_plugins_from_dict

    Returns:
    --------

    A PluginsInstances object with the plugin objects created

    """
    return new_plugins_from_dict(
        config=config, type=Type.OUTPUT, plugin_list=output_list)


def new_output_from_dict(
        config: Config, output_dict: Dict[str, Any]) -> OutputBase:
    """ Create a single output plugin from a Dict of information for it

    Create a new output plugin from a map/dict of settings for the needed parameters.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    output_dict (Dict[str,Any]) : Dict from which all needed information will
        be pulled.  Optionally additional config sources can be included as well
        as arguments which could be passed to the plugin.

        @see new_plugin_from_dict for more details.

    Return:
    -------

    A plugin object (OutputBase)

    """
    return new_plugin_from_dict(
        config=config, type=Type.OUTPUT, plugin_dict=output_dict)


def new_output(config: Config, plugin_id: str,
               instance_id: str) -> OutputBase:
    """ Create a new output from parameters

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    plugin_id (str) : UCTT plugin id for the output type, to tell us what plugin
        factory to load.

        @see .plugin.Factory for more details on how plugins are loaded.

    instance_id (str) : string instance id that will be passed to the new plugin
        object.

    Return:
    -------

    A plugin object (OutputBase)

    """
    return new_plugin(config=config, type=Type.OUTPUT,
                      plugin_id=plugin_id, instance_id=instance_id)


""" WORKLOAD CONSTRUCTION """


def new_workloads_from_config(config: Config,
                              label: str = UCTT_WORKLOAD_CONFIG_WORKLOADS_LABEL,
                              base: Any = LOADED_KEY_ROOT) -> PluginInstances:
    """ Create workloads from some config

    This method will interpret some config values as being usable to build
    a PluginInstances set of workload plugins

    Parameters:
    -----------

    config (Config) : Used to load and get the workload configuration

    label (str) : config label to load to pull workload configuration. That
        label is loaded and config is pulled to produce a list of workloads

    base (str|List) : config key to get a Dict of plugins configurations.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    Returns:
    --------

    PluginInstances of workload plugins

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugins_from_config(
        config=config, type=Type.WORKLOAD, label=label, base=base)


def new_workload_from_config(config: Config,
                             label: str = UCTT_WORKLOAD_CONFIG_WORKLOAD_LABEL,
                             base: Any = LOADED_KEY_ROOT) -> WorkloadBase:
    """ Create a workload from some config

    This method will interpret some config values as being usable to build
    workload

    Parameters:
    -----------

    config (Config) : Used to load and get the workload configuration

    label (str) : config label to load to pull workload configuration. That
        label is loaded and config is pulled to produce a list of workloads

    base (str|List) : config key to get a Dict of plugin configuration.
        A list of strings is valid as configerus.loaded.get() can take that as
        an argument.
        We call this base instead of key as we will be searching for sub-paths
        to pull individual elements

    Returns:
    --------

    workload plugin (WorkloadBase)

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugin_from_config(
        config=config, type=Type.WORKLOAD, label=label, base=base)


def new_workloads_from_dict(
        config: Config, workload_list: Dict[str, Dict]) -> PluginInstances:
    """ Create a set of workload plugins from Dict information

    The passed dict should be a key=>details map of workloads, which will be turned
    into a PluginInstances map of plugins that can be used to interact with the
    objects.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    workload_list (Dict[str, Dict]) : map of key=> config dicts, where each dict
        contains all of the information that is needed to build the plugin.

        for details, @see new_plugins_from_dict

    Returns:
    --------

    A PluginsInstances object with the plugin objects created

    """
    return new_plugins_from_dict(
        config=config, type=Type.WORKLOAD, plugin_list=workload_list)


def new_workload_from_dict(
        config: Config, workload_dict: Dict[str, Any]) -> WorkloadBase:
    """ Create a single workload plugin from a Dict of information for it

    Create a new workload plugin from a map/dict of settings for the needed parameters.

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    workload_dict (Dict[str,Any]) : Dict from which all needed information will
        be pulled.  Optionally additional config sources can be included as well
        as arguments which could be passed to the plugin.

        @see new_plugin_from_dict for more details.

    Return:
    -------

    A plugin object (WorkloadBase)

    """
    return new_plugin_from_dict(
        config=config, type=Type.WORKLOAD, plugin_dict=workload_dict)


def new_workload(config: Config, plugin_id: str,
                 instance_id: str) -> WorkloadBase:
    """ Create a new workload from parameters

    Parameters:
    -----------

    config (Config) : configerus.Config object passed to each generated plugins.

    plugin_id (str) : UCTT plugin id for the workload type, to tell us what plugin
        factory to load.

        @see .plugin.Factory for more details on how plugins are loaded.

    instance_id (str) : string instance id that will be passed to the new plugin
        object.

    Return:
    -------

    A plugin object (WorkloadBase)

    """
    return new_plugin(config=config, type=Type.WORKLOAD,
                      plugin_id=plugin_id, instance_id=instance_id)
