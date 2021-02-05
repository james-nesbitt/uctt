"""

MTT Kubernetes

MTT contrib functionality for Kubernetes.  In particular to provide plugins for
kubernetes clients and kubernetes workloads.

"""

import os
from configerus.config import Config

from uctt import plugin as uctt_plugin

from .plugins.client import KubernetesClientPlugin
from .plugins.workload import KubernetesSpecFilesWorkloadPlugin

UCTT_PLUGIN_ID_KUBERNETES_CLIENT='mtt_kubernetes'
""" client plugin_id for the mtt dummy plugin """
@uctt_plugin.Factory(type=uctt_plugin.Type.CLIENT, plugin_id=UCTT_PLUGIN_ID_KUBERNETES_CLIENT)
def uctt_plugin_factory_client_kubernetes(config:Config, instance_id:str = ''):
    """ create an mtt kubernetes client plugin """
    return KubernetesClientPlugin(config, instance_id)


UCTT_PLUGIN_ID_KUBERNETES_SPEC_WORKLAOD='mtt_kubernetes_spec'
""" workload plugin_id for the mtt_kubernetes spec plugin """
@uctt_plugin.Factory(type=uctt_plugin.Type.WORKLOAD, plugin_id=UCTT_PLUGIN_ID_KUBERNETES_SPEC_WORKLAOD)
def uctt_plugin_factory_workload_kubernetes_spec(config:Config, instance_id:str = ''):
    """ create an mtt kubernetes spec workload plugin """
    return KubernetesSpecFilesWorkloadPlugin(config, instance_id)

""" SetupTools EntryPoint BootStrapping """

def uctt_bootstrap(config:Config):
    """ UCTT_Kubernetes bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass

def configerus_bootstrap(config:Config):
    """ UCTT_Kubernetes configerus bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorators to register our plugins.

    """
    pass
