"""

Docker workloads plugin

"""
from typing import Dict, Any
import logging

from uctt.plugin import Type
from uctt.environment import Environment
from uctt.fixtures import Fixtures
from uctt.workload import WorkloadBase

logger = logging.getLogger('uctt.contrib.docker.workload.run')

DOCKER_RUN_WORKLOAD_CONFIG_LABEL = 'docker'
""" Configerus label for retrieving docker run workloads """
DOCKER_RUN_WORKLOAD_CONFIG_BASE = 'workload.run'
""" Configerus get base for retrieving the default run workload """


class DockerRunWorkloadPlugin(WorkloadBase):
    """ Docker Run workload class """

    def __init__(self, environment: Environment, instance_id: str,
                 label: str = DOCKER_RUN_WORKLOAD_CONFIG_LABEL, base: Any = DOCKER_RUN_WORKLOAD_CONFIG_BASE):
        """ Run the super constructor but also set class properties

        Parameters:
        -----------

        outputs (Dict[Dict]) : pass in a dictionary which defines outputs that
            should be returned

        clients (Dict[Dict]) : pass in a dictionary which defines which clients
            should be requested when working on a provisioner

        """
        WorkloadBase.__init__(self, environment, instance_id)

        logger.info("Preparing Docker run setting")

        self.config_label = label
        """ configerus load label that should contain all of the config """
        self.config_base = base
        """ configerus get key that should contain all tf config """

        self.loaded_config = self.environment.config.load(self.config_label)
        """ get a configerus LoadedConfig for the docker run label """

        self.docker_client_fixture = None
        """ This workload needs only a docker client fixture/plugin """

    def set_fixtures(self, fixtures: Fixtures):
        """ Retrieve fixtures from a set of Fixtures

        Parameters:
        -----------

        fixtures (Fixtures) : a set of fixtures that this workload will use to
            retrieve a docker client plugin.

        """

        self.docker_client_fixture = fixtures.get_fixture(
            type=Type.CLIENT, plugin_id='uctt_docker')

    def apply(self):
        """ Run the workload

        @NOTE Needs a docker client fixture to run.  Use .set_fixtures() first

        """

        if self.docker_client_fixture is None:
            raise ValueError(
                "No docker client was attached to the workload before exec()")

        client = self.docker_client_fixture.plugin
        run = self.loaded_config.get([self.config_base, 'run'])

        assert 'image' in run, "Run command had no image"

        return client.containers.run(**run)
