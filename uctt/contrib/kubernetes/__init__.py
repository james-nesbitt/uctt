"""

MTT Kubernetes

MTT contrib functionality for Kubernetes.  In particular to provide plugins for
kubernetes clients and kubernetes workloads.

"""

import os
from typing import List, Any

from uctt.plugin import Factory, Type
from uctt.environment import Environment

from .client import KubernetesClientPlugin
from .deployment_workload import KubernetesDeploymentWorkloadPlugin, KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_LABEL, KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_BASE

UCTT_PLUGIN_ID_KUBERNETES_CLIENT = 'uctt_kubernetes'
""" client plugin_id for the mtt dummy plugin """


@Factory(type=Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_KUBERNETES_CLIENT)
def uctt_plugin_factory_client_kubernetes(
        environment: Environment, instance_id: str = '', kube_config_file: str = ''):
    """ create an mtt kubernetes client plugin """
    return KubernetesClientPlugin(environment, instance_id, kube_config_file)


UCTT_PLUGIN_ID_KUBERNETES_DEPLOYMENT_WORKLAOD = 'uctt_kubernetes_deployment'
""" workload plugin_id for the mtt_kubernetes deployment plugin """


@Factory(type=Type.WORKLOAD,
         plugin_id=UCTT_PLUGIN_ID_KUBERNETES_DEPLOYMENT_WORKLAOD)
def uctt_plugin_factory_workload_kubernetes_deployment(
        environment: Environment, instance_id: str = '', label: str = KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_LABEL, base: Any = KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_BASE):
    """ create an mtt kubernetes spec workload plugin """
    return KubernetesDeploymentWorkloadPlugin(
        environment, instance_id, label=label, base=base)


""" SetupTools EntryPoint UCTT BootStrapping """


def bootstrap(environment: Environment):
    """ UCTT_Kubernetes bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
