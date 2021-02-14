"""

MTT Docker

MTT contrib package for docker functionality, specifically for registering
a Docker client plugin.

"""

import os

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .client import DockerClientPlugin

UCTT_PLUGIN_ID_DOCKER_CLIENT = 'mtt_docker'
""" client plugin_id for the mtt dummy plugin """


@Factory(type=Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_DOCKER_CLIENT)
def uctt_plugin_factory_client_docker(
    environment: Environment, instance_id: str = '', host: str = '', cert_path: str = '', tls_verify: bool = True,
        compose_tls_version: str = 'TLSv1_2'):
    """ create an mtt client dict plugin """
    return DockerClientPlugin(environment, instance_id,
                              host, cert_path, tls_verify, compose_tls_version)


""" SetupTools EntryPoint UCTT BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT_Docker bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
