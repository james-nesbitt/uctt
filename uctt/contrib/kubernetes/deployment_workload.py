"""

Kubernetes workload plugins

"""

import logging
from typing import List, Any

import kubernetes

from uctt.plugin import Type
from uctt.fixtures import Fixtures
from uctt.workload import WorkloadBase

from .client import KubernetesClientPlugin

logger = logging.getLogger('uctt.contrib.kubernetes.workload.deployment')

KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_LABEL = 'kubernetes'
KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_BASE = 'workload.deployment'

KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_KEY_NAMESPACE = "namespace"
KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_KEY_BODY = "body"


class KubernetesDeploymentWorkloadPlugin(WorkloadBase):
    """ Kubernetes workload class """

    def __init__(self, environment, instance_id,
                 label: str = KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_LABEL, base: Any = KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_BASE):
        """ Run the super constructor but also set class properties

        This implements the args part of the client interface.

        Here we expect to receive a path to a KUBECONFIG file with a context set
        and we create a Kubernetes client for use.  After that this can provide
        Core api clients as per the kubernetes SDK

        Parameters:
        -----------

        config_file (str): String path to the kubernetes config file to use

        """
        WorkloadBase.__init__(self, environment, instance_id)

        self.config_label = label
        """ configerus load label that should contain all of the config """
        self.config_base = base
        """ configerus get key that should contain all tf config """

        self.kubernetes_client_fixture = None
        self.deployment = None

    def set_fixtures(self, fixtures: Fixtures):
        """ Retrieve fixtures from a set of Fixtures

        Parameters:
        -----------

        fixtures (Fixtures) : a set of fixtures that this workload will use to
            retrieve a docker client plugin.

        """

        self.kubernetes_client_fixture = fixtures.get_fixture(
            type=Type.CLIENT, plugin_id='uctt_kubernetes')

    def apply(self):
        """ Run the workload

        @NOTE Needs a kubernetes client fixture to run.  Use .set_fixtures() first

        """

        if self.kubernetes_client_fixture is None:
            raise ValueError(
                "No kubernetes client was attached to the workload before exec()")

        workload_config = self.environment.config.load(self.config_label)

        namespace = workload_config.get(
            [self.config_base, KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_KEY_NAMESPACE])
        body = workload_config.get(
            [self.config_base, KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_KEY_BODY])

        k8s_apps_v1 = kubernetes.client.AppsV1Api(
            self.kubernetes_client_fixture.plugin.api_client)
        self.deployment = k8s_apps_v1.create_namespaced_deployment(
            body=body, namespace=namespace)

        return self.deployment

    def destroy(self):
        """ destroy any created resources """

        if self.kubernetes_client_fixture is None:
            raise ValueError(
                "No kubernetes client was attached to the workload before exec()")

        workload_config = self.environment.config.load(self.config_label)

        # if we have a deployment registered, pull its name directly, otherwise assume that
        # the config metadata name is correct (we could be cleaning up previous
        # runs)
        if self.deployment is not None:
            name = self.deployment.metadata.name
        else:
            name = workload_config.get(
                [self.config_base, KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_KEY_BODY, 'metadata.name'])
        namespace = workload_config.get(
            [self.config_base, KUBERNETES_DEPLOYMENT_WORKLOAD_CONFIG_KEY_NAMESPACE])
        body = kubernetes.client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5)

        k8s_apps_v1 = kubernetes.client.AppsV1Api(
            self.kubernetes_client_fixture.plugin.api_client)
        self.status = k8s_apps_v1.delete_namespaced_deployment(
            name=name, namespace=namespace, body=body)

        return self.status
