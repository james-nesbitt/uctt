import logging

from configerus.config import Config

from .plugin import MTTPlugin, Type as PluginType, Factory as PluginFactory

logger = logging.getLogger('uctt.output')

UCTT_PLUGIN_ID_OUTPUT = PluginType.OUTPUT
""" Fast access to the output plugin type """

class OutputBase(MTTPlugin):
    """ Base class for output plugins """
    pass

def make_output(plugin_id:str, config:Config, instance_id:str = ''):
    """ Create a new output plugin

    Parameters:
    -----------

    plugin_id (str) : what output plugin should be created

    config (Config) : config object to pass to the plugin constructor
    instance_id(str) : instance_id to pass to the plugin constructor

    Returns:
    --------

    A output plugin instance

    Throws:
    -------

    Can throw a NotImplementedError if you asked for a plugin_id that has not
    been registered.

    """
    logger.debug("Creating output plugin: %s:%s".format(plugin_id, instance_id))
    try:
        output_factory = PluginFactory(UCTT_PLUGIN_ID_OUTPUT, plugin_id)
        output = output_factory.create(config, instance_id)

    except NotImplementedError as e:
        raise NotImplementedError("Could not create output '{}' as that plugin_id could not be found.".format(plugin_id)) from e
    except Exception as e:
        raise Exception("Could not create output '{}' as the plugin factory produced an exception".format(plugin_id)) from e

    if not isinstance(output, OutputBase):
        logger.warn("Created output plugin does not extend the OutputBase")

    return output
