"""

MTT Kubernetes

MTT contrib functionality for Kubernetes.  In particular to provide plugins for
kubernetes clients and kubernetes workloads.

"""

import os
from typing import List

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .client import KubernetesClientPlugin
from .workload import KubernetesSpecFilesWorkloadPlugin

UCTT_PLUGIN_ID_KUBERNETES_CLIENT = 'mtt_kubernetes'
""" client plugin_id for the mtt dummy plugin """


@Factory(type=Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_KUBERNETES_CLIENT)
def uctt_plugin_factory_client_kubernetes(
        environment: Environment, instance_id: str = '', kube_config_file: str = ''):
    """ create an mtt kubernetes client plugin """
    return KubernetesClientPlugin(environment, instance_id, kube_config)


UCTT_PLUGIN_ID_KUBERNETES_SPEC_WORKLAOD = 'mtt_kubernetes_spec'
""" workload plugin_id for the mtt_kubernetes spec plugin """


@Factory(type=Type.WORKLOAD, plugin_id=UCTT_PLUGIN_ID_KUBERNETES_SPEC_WORKLAOD)
def uctt_plugin_factory_workload_kubernetes_spec(
        environment: Environment, instance_id: str = '', files: List[str] = []):
    """ create an mtt kubernetes spec workload plugin """
    return KubernetesSpecFilesWorkloadPlugin(environment, instance_id, files)


""" SetupTools EntryPoint UCTT BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT_Kubernetes bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
