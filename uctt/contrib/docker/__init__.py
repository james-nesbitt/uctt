"""

MTT Docker

MTT contrib package for docker functionality, specifically for registering
a Docker client plugin.

"""

from typing import Any

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .client import DockerClientPlugin
from .run_workload import DockerRunWorkloadPlugin, DOCKER_RUN_WORKLOAD_CONFIG_LABEL, DOCKER_RUN_WORKLOAD_CONFIG_BASE

UCTT_PLUGIN_ID_DOCKER_CLIENT = 'uctt_docker'
""" client plugin_id for the mtt dummy plugin """


@Factory(type=Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_DOCKER_CLIENT)
def uctt_plugin_factory_client_docker(
    environment: Environment, instance_id: str = '', host: str = '', cert_path: str = '', tls_verify: bool = True,
        compose_tls_version: str = 'TLSv1_2', version: str = 'auto'):
    """ create an mtt client dict plugin """
    return DockerClientPlugin(environment, instance_id=instance_id,
                              host=host, cert_path=cert_path, tls_verify=tls_verify, compose_tls_version=compose_tls_version, version=version)


UCTT_PLUGIN_ID_DOCKER_RUN_WORKLOAD = 'uctt_docker_run'
""" workload plugin_id for the docker run plugin """


@Factory(type=Type.WORKLOAD, plugin_id=UCTT_PLUGIN_ID_DOCKER_RUN_WORKLOAD)
def uctt_plugin_factory_workload_docker_run(
        environment: Environment, instance_id: str = '', label: str = DOCKER_RUN_WORKLOAD_CONFIG_LABEL, base: Any = DOCKER_RUN_WORKLOAD_CONFIG_BASE):
    """ create a docker run workload plugin """
    return DockerRunWorkloadPlugin(
        environment, instance_id, label=label, base=base)


""" SetupTools EntryPoint UCTT BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT_Docker bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
