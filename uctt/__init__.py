from importlib import metadata
from typing import Dict, List, Any
import logging

from configerus.config import Config
from configerus.contrib.dict import PLUGIN_ID_CONFIGSOURCE_DICT

from .plugin import Type, PluginInstances
from .provisioner import make_provisioner, ProvisionerBase
from .workload import WorkloadBase
from .client import ClientBase
from .output import OutputBase

import uctt.contrib.common

logger = logging.getLogger("uctt")

""" BOOTSTRAPPING """

UCTT_BOOTSTRAP_ENTRYPOINT = "uctt.bootstrap"
""" SetupTools entry_point used for UCTT bootstrap """

def bootstrap(config:Config, bootstraps=[]):
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
            raise KeyError("Bootstrap not found {}:{}".format(UCTT_BOOTSTRAP_ENTRYPOINT, bootstrap_id))

""" PROVISIONER Construction """

UCTT_PROVISIONER_CONFIG_LABEL_DEFAULT = 'provisioner'
""" provisioner_from_config will load this config to decide how to build the provisioner plugin """
UCTT_PROVISIONER_CONFIG_KEY_PLUGINID = 'plugin_id'
""" provisioner_from_config will .get() this key from the provisioner config to decide what plugin to create """
UCTT_PROVISIONER_FROMCONFIG_INSTANCEID_DEFAULT = 'fromconfig'
""" what plugin instance_id to use for the provisioner from config """
def new_provisioner_from_config(
        config:Config,
        instance_id:str=UCTT_PROVISIONER_FROMCONFIG_INSTANCEID_DEFAULT,
        config_label:str=UCTT_PROVISIONER_CONFIG_LABEL_DEFAULT) -> ProvisionerBase:
    """ Create a new provisioner plugin from a config object

    The config object is used decide what plugin to load.

    First we config.load('provisioner')
    and then we ask for .get('plugin_id')

    Parameters:
    -----------

    config (Config) : used to decide what provisioner plugin to load, and also
        passed to the provisioner plugin

    instance_id (str) : give the provisioner plugins instance a specific name

    config_label (str) : load provisioner config from a specific config label
        This allows you to configure multiple provisioners using a different
        label per provisioner.

    Returns:
    --------

    a provisioner plugin instance created by the decorated factory method that
    was registered for the plugin_id

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to get
    a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    See mtt_dummy for examples
    """

    prov_config = config.load(config_label)
    plugin_id = prov_config.get(UCTT_PROVISIONER_CONFIG_KEY_PLUGINID)

    return make_provisioner(plugin_id, config, instance_id)

def new_provisioner_from_plugin_id(plugin_id:str, config:Config, instance_id:str=UCTT_PROVISIONER_FROMCONFIG_INSTANCEID_DEFAULT) -> ProvisionerBase :
    """ Make a new provisioner from a plugin id """
    return make_provisioner(plugin_id, config, instance_id)

""" WORKLOAD Construction """

UCTT_WORKLOAD_CONFIG_LABEL = 'workloads'
""" new_workloads_from_config will load this config to decide how to build the worklaod plugin """
UCTT_WORKLOAD_CONFIG_KEY_WORKLOADS = 'workloads'
""" new_workloads_from_config will get() this config to decide how to build each worklaod plugin """
UCTT_WORKLOAD_CONFIG_KEY_PLUGINID = 'plugin_id'
""" new_workloads_from_config will use this Dict key from the worklaod config to decide what plugin to create """
UCTT_WORKLOAD_CONFIG_KEY_INSTANCEID = 'instance_id'
""" neww_workloads_from_config will use this Dict key assign an instance_id """
UCTT_WORKLOAD_CONFIG_KEY_INSTANCEID = 'instance_id'
""" neww_workloads_from_config will use this Dict key assign an instance_id """
UCTT_WORKLOAD_CONFIG_KEY_CONFIG = 'config'
""" new_workloads_from_config will use this Dict key as additional config """
UCTT_WORKLOAD_CONFIG_KEY_ARGS = 'arguments'
""" new_workloads_from_config will use this Dict key for arguments to pass to the plugin """
def new_workloads_from_config(config:Config,
        label:str=UCTT_WORKLOAD_CONFIG_LABEL,
        key:str=UCTT_WORKLOAD_CONFIG_KEY_WORKLOADS) -> PluginInstances:
    """ Retrieve a keyed Dict of workload plugins from config

    the config object is used to retrieve workload settings.  A Dict of workload
    plugin conf is loaded, and each config is turned into a plugin.

    Parameters:
    -----------

    config (Config) : Used to load and get the workload configuration

    label (str) : config label to load to pull workload configuration. That
        label is loaded and config is pulled to produce a list of workloads

    key (str) : config key to get a Dict of workload configurations.

    Returns:
    --------

    Dict[str, WorkloadBase] of workload plugins

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugins_from_config(config, Type.WORKLOAD, label, key)

def new_workload_from_dict(workload_dict:Dict[str, Any], config:Config) -> WorkloadBase:
    """ Create a workload plugin from a dict of workload data """
    return new_plugins_from_dict(workload_dict, Type.WORKLOAD, config)

""" CLIENT CONSTRUCTION """

UCTT_CLIENT_CONFIG_LABEL = 'clients'
""" pclients_from_config will load this config to decide how to build the provisioner plugin """
UCTT_CLIENT_CONFIG_KEY_CLIENTS = 'clients'
""" clients will get() this config to decide how to build each provisioner plugin """
UCTT_CLIENT_CONFIG_KEY_PLUGINID = 'plugin_id'
""" clients_from_config will use this Dict key from the client config to decide what plugin to create """
UCTT_CLIENT_CONFIG_KEY_INSTANCEID = 'instance_id'
""" clients_from_config will use this Dict key assign an instance_id """
UCTT_CLIENT_CONFIG_KEY_CONFIG = 'config'
""" new_clients_from_config will use this Dict key as additional config """
UCTT_CLIENT_CONFIG_KEY_ARGS = 'arguments'
""" new_clients_from_config will use this Dict key from the client config to decide what arguments to pass to the plugin """
def new_clients_from_config(config:Config,
        label:str=UCTT_CLIENT_CONFIG_LABEL,
        key:str=UCTT_CLIENT_CONFIG_KEY_CLIENTS) -> PluginInstances:
    """ Create clients from some config

    This method will interpret some config values as being usable to build a Dict
    of clients from.

    Parameters:
    -----------

    config (Config) : Used to load and get the client configuration

    label (str) : config label to load to pull client configuration. That
        label is loaded and config is pulled to produce a list of clients

    key (str) : config key to get a Dict of clients configurations.

    Returns:
    --------

    Dict[str, WorkloadBase] of workload plugins

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugins_from_config(config, Type.CLIENT, label, key)

def new_clients_from_dict(client_list:Dict[str,Dict], config:Config) -> PluginInstances:
    """ Create a dict of client plugins from Dict information """
    return new_plugins_from_dict(client_list, Type.CLIENT, config)

def new_client_from_dict(client_dict:Dict[str, Any], config:Config) -> ClientBase:
    """ Create a new client from a Dict of information for it """
    plugin_id = client_dict[UCTT_CLIENT_CONFIG_KEY_PLUGINID]
    instance_id = client_dict[UCTT_CLIENT_CONFIG_KEY_INSTANCEID]

    instance_config = config
    # If we were given a client config, then create a copy of the config
    # object and add the passed config as new sources to the copy
    if UCTT_CLIENT_CONFIG_KEY_CONFIG in client_dict:
        instance_config = config.copy()
        # Add a dict source plugin for the passed 'config', giving it source id
        # just to make identification easier
        instance_config.add_source(PLUGIN_ID_CONFIGSOURCE_DICT, 'client-{}-{}'.format(plugin_id,instance_id)).set_data(client_dict[UCTT_CLIENT_CONFIG_KEY_CONFIG])

    client = make_client(plugin_id, instance_config, instance_id)

    if UCTT_CLIENT_CONFIG_KEY_ARGS in client_config:
        client.arguments(**clients_config[UCTT_CLIENT_CONFIG_KEY_ARGS])

    return client


""" OUTPUT CONSTRUCTION """

UCTT_OUTPUT_CONFIG_LABEL = 'outputs'
""" poutputs_from_config will load this config to decide how to build the provisioner plugin """
UCTT_OUTPUT_CONFIG_KEY_OUTPUTS = 'outputs'
""" outputs will get() this config to decide how to build each provisioner plugin """
UCTT_OUTPUT_CONFIG_KEY_PLUGINID = 'plugin_id'
""" outputs_from_config will use this Dict key from the output config to decide what plugin to create """
UCTT_OUTPUT_CONFIG_KEY_INSTANCEID = 'instance_id'
""" outputs_from_config will use this Dict key assign an instance_id """
UCTT_OUTPUT_CONFIG_KEY_CONFIG = 'config'
""" new_outputs_from_config will use this Dict key as additional config """
UCTT_OUTPUT_CONFIG_KEY_ARGS = 'arguments'
""" new_outputs_from_config will use this Dict key from the output config to decide what arguments to pass to the plugin """
def new_outputs_from_config(config:Config,
        label:str=UCTT_OUTPUT_CONFIG_LABEL,
        key:str=UCTT_OUTPUT_CONFIG_KEY_OUTPUTS) -> PluginInstances:
    """ Create outputs from some config

    This method will interpret some config values as being usable to build a Dict
    of outputs from.

    Parameters:
    -----------

    config (Config) : Used to load and get the output configuration

    label (str) : config label to load to pull output configuration. That
        label is loaded and config is pulled to produce a list of outputs

    key (str) : config key to get a Dict of outputs configurations.

    Returns:
    --------

    Dict[str, WorkloadBase] of workload plugins

    Raises:
    -------

    If you ask for a plugin which has not been registered, then you're going to
    get a NotImplementedError exception.
    To make sure that your desired plugin is registered, make sure to import
    the module that contains the factory method with a decorator.

    """
    return new_plugins_from_config(config, Type.OUTPUT, label, key)

def new_outputs_from_dict(output_list:Dict[str,Dict], config:Config) -> PluginInstances:
    """ Create a dict of output plugins from Dict information """
    return new_plugins_from_dict(output_list, Type.OUTPUT, config)

def new_output_from_dict(output_dict:Dict[str, Any], config:Config) -> OutputBase:
    """ Create a new output from a Dict of information for it """
    plugin_id = output_dict[UCTT_OUTPUT_CONFIG_KEY_PLUGINID]
    instance_id = output_dict[UCTT_OUTPUT_CONFIG_KEY_INSTANCEID]

    instance_config = config
    # If we were given a output config, then create a copy of the config
    # object and add the passed config as new sources to the copy
    if UCTT_OUTPUT_CONFIG_KEY_CONFIG in output_dict:
        instance_config = config.copy()
        # Add a dict source plugin for the passed 'config', giving it source id
        # just to make identification easier
        instance_config.add_source(PLUGIN_ID_CONFIGSOURCE_DICT, 'output-{}-{}'.format(plugin_id,instance_id)).set_data(output_dict[UCTT_OUTPUT_CONFIG_KEY_CONFIG])

    output = make_output(plugin_id, instance_config, instance_id)

    if UCTT_OUTPUT_CONFIG_KEY_ARGS in output_config:
        output.arguments(**outputs_config[UCTT_OUTPUT_CONFIG_KEY_ARGS])

    return output

""" Generic Plugin construction """


""" PLUGIN CONSTRUCTION """

UCTT_PLUGIN_CONFIG_KEY_PLUGINID = 'plugin_id'
""" plugins_from_config will use this Dict key from the plugin config to decide what plugin to create """
UCTT_PLUGIN_CONFIG_KEY_INSTANCEID = 'instance_id'
""" plugins_from_config will use this Dict key assign an instance_id """
UCTT_PLUGIN_CONFIG_KEY_CONFIG = 'config'
""" new_plugins_from_config will use this Dict key as additional config """
UCTT_PLUGIN_CONFIG_KEY_ARGS = 'arguments'
""" new_plugins_from_config will use this Dict key from the plugin config to decide what arguments to pass to the plugin """
def new_plugins_from_config(config:Config, type:Type, label:str, key:str) -> PluginInstances:
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

    return new_plugins_from_dict(plugin_list, type, config)

def new_plugins_from_dict(plugin_list:Dict[str,Dict[str,Any]], type:Type, config:Config) -> PluginInstances:
    """ Create a dict of plugins from Dict information """
    plugins = PluginInstances(config=config)

    if not isinstance(plugin_list, dict):
        raise ValueError('Did not receive a good dict of config to make plugins from: %s', plugin_list)

    for instance_id, plugin_config in plugin_list.items():
        if not isinstance(plugin_config, dict):
            raise ValueError("Recevied bad plugin configuration, expected Dict[str,Any], got '{}'".format(plugin_config))

        plugin_id = plugin_config[UCTT_WORKLOAD_CONFIG_KEY_PLUGINID]

        instance_config = config
        # If we were given plugin config, then create a copy of the config
        # object and add the passed config as new sources to the copy
        if UCTT_PLUGIN_CONFIG_KEY_CONFIG in plugin_config:
            instance_config = config.copy()
            instance_config.add_source(PLUGIN_ID_CONFIGSOURCE_DICT, 'plugin-{}'.format(plugin_id)).set_data(plugin_config[UCTT_PLUGIN_CONFIG_KEY_CONFIG])

        plugin = plugins.add_plugin(type, plugin_id, instance_id, 60, instance_config)
        if not plugin:
            raise Exception("Did not create a good plugin")

        if UCTT_PLUGIN_CONFIG_KEY_ARGS in plugin_config:
            try:
                arguments = plugin_config[UCTT_PLUGIN_CONFIG_KEY_ARGS]
                plugin.arguments(**arguments)
            except Exception as e:
                raise Exception("Plugin [{}] did not like the arguments given: {}".format(plugin, e))

    return plugins
