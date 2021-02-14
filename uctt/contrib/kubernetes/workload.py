"""

Kubernetes workload plugins

"""

import logging
from typing import List

from kubernetes import utils as kubernetes_utils

from uctt.workload import WorkloadBase

from .client import KubernetesClientPlugin

logger = logging.getLogger('uctt.contrib.kubernetes.workload')


class KubernetesSpecFilesWorkloadPlugin(WorkloadBase):
    """ Kubernetes workload class """

    def __init__(self, environment, instance_id, files: List[str] = []):
        """ Run the super constructor but also set class properties

        This implements the args part of the client interface.

        Here we expect to receive a path to a KUBECONFIG file with a context set
        and we create a Kubernetes client for use.  After that this can provide
        Core api clients as per the kubernetes SDK

        Parameters:
        -----------

        config_file (str): String path to the kubernetes config file to use

        """
        super(ClientBase, self).__init__(environment, instance_id)

        self.set_files(files)

    def set_files(files: List[str]):
        """ include a list of kubernetes yaml files to be used in this workload """
        self.files = files

    def apply(client: KubernetesClientPlugin):
        """ exec the workload on a client """
        for file in self.files:
            kubernetes_utils.utils.create_from_yaml(client, file)

    def destroy(client: KubernetesClientPlugin):
        """ Remove any resources created in apply """
        logger.warn(
            "KubernetesSpecFilesWorkloadPlugin.destroy() not written yet")
