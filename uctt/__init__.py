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

from configerus import new_config as configerus_new_config
from configerus.config import Config

from .environment import Environment

logger = logging.getLogger('uctt')

""" UCTT and Configerus bootstrapping """

FIXED_CONFIGERUS_BOOSTRAPS = [
    "deep",
    "get",
    "jsonschema",
    "files"
]
""" configerus bootstraps that we will use on config objects """
FIXED_UCTT_BOOTSTRAPS = [
    "uctt_validation",
    "uctt_common",
    "uctt_dummy"
]
DEFAULT_ADDITIONAL_UCTT_BOOTSTRAPS = [
    "uctt_ansible",
    "uctt_docker",
    "uctt_kubernetes",
    "uctt_terraform"
]
""" default overridable uctt bootstrap calls """

DEFAULT_ENVIRONMENT_NAME = 'default'
""" If you don't ask for a particular environment, you are going to get this one """

""" Environments """

_environments = {}
""" Keep a Dict of all created environments for introspection """


def new_environment(name: str = DEFAULT_ENVIRONMENT_NAME, additional_uctt_bootstraps: List[str] = DEFAULT_ADDITIONAL_UCTT_BOOTSTRAPS,
                    additional_configerus_bootstraps: List[str] = []):
    """ Make new environment object

    First create a config object, then use it to create an environment
    object.

    Parameters
    ----------

    additional_uctt_bootstraps (List[str]) : run additiional uctt bootstraps
        on the config object.  Defaults to the mtt bootstrap.

    additional_configerus_bootstraps (List[str]) : run additional configerus
        bootstrap entry_points

    Returns:
    --------

    An initialized Environment object with a new configerus Config object

    """
    configerus_bootstraps_unique = list(
        set(FIXED_CONFIGERUS_BOOSTRAPS + additional_configerus_bootstraps))
    config = configerus_new_config(bootstraps=configerus_bootstraps_unique)

    return new_environment_from_config(
        name=name, config=config, additional_uctt_bootstraps=additional_uctt_bootstraps)


def new_environment_from_config(config: Config,
                                name: str = DEFAULT_ENVIRONMENT_NAME, additional_uctt_bootstraps: List[str] = DEFAULT_ADDITIONAL_UCTT_BOOTSTRAPS):
    """ Make a new environment from an existing configerus.Config object

    Use a passed configerus Config object to create an environment object,
    register the env and then return it.

    The config object is bootstrapped before we create the environment.

    Parameters
    ----------

    additional_uctt_bootstraps (List[str]) : run additiional uctt bootstraps
        on the config object.  Defaults to the mtt bootstrap.

    additional_configerus_bootstraps (List[str]) : run additional configerus
        bootstrap entry_points

    Returns:
    --------

    An intialized Environment object from the config

    """
    global _environments

    environment = Environment(config=config)

    uctt_bootstraps_unique = list(
        set(FIXED_UCTT_BOOTSTRAPS + additional_uctt_bootstraps))
    bootstrap(environment, uctt_bootstraps_unique)

    if name in _environments:
        logger.warn(
            "Existing environment '{}' is being overwritten".format(name))
    _environments[name] = environment
    return environment


def environment_names() -> List[str]:
    """ Return a list of all of the created environments """
    return list(_environments)


def has_environment(name: str) -> bool:
    """ Does an environment already exist with a passed name """
    return name in _environments.keys()


def get_environment(name: str = DEFAULT_ENVIRONMENT_NAME) -> Environment:
    """ Return an environment that has already been created """
    try:
        return _environments[name]
    except KeyError as e:
        raise KeyError(
            "Requested environment has not yet been created: {}".format(name)) from e


""" BOOTSTRAPPING """

UCTT_BOOTSTRAP_ENTRYPOINT = 'uctt.bootstrap'
""" SetupTools entry_point used for UCTT bootstrap """


def bootstrap(environment: Environment, bootstraps=[]):
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

    environment (environment.Environment) : Environment which bootstrap can
        modify.

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
                plugin(environment)
                break
        else:
            raise KeyError(
                "Bootstrap not found {}:{}".format(
                    UCTT_BOOTSTRAP_ENTRYPOINT,
                    bootstrap_id))
