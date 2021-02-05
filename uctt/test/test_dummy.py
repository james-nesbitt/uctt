"""

DUMMY Plugin testing.

As toolbox operations are quite context sensitive, and could involve creating
infrastructure, we don't have unit testing for them

Here we test the overall toolbox workflows using dummy plugins.

"""
import logging
import unittest
# Configerus imports needed to create a config object
import configerus
from configerus.contrib.dict import PLUGIN_ID_CONFIGSOURCE_DICT
# UCTT components we will need to access the toolbox
import uctt
# We import this so that we don't need to guess on plugin_ids, but not needed
from uctt.contrib.dummy import UCTT_PLUGIN_ID_DUMMY

# imports used only for type testing
from uctt.contrib.dummy.plugins.provisioner import DummyProvisionerPlugin
from uctt.contrib.dummy.plugins.workload import DummyWorkloadPlugin

logger = logging.getLogger("test_dummy")
logger.setLevel(logging.INFO)

""" Contents of test config files used as the source for a config object """

""" TESTS """

class ConfigTemplating(unittest.TestCase):

    def _dummy_config(self):
        """ Create a config object for dummy conventions """

        config = configerus.new_config()
        uctt.bootstrap(config, ['uctt_dummy']) # not strictly necessary
        config.add_source(PLUGIN_ID_CONFIGSOURCE_DICT).set_data({
            'provisioner': {
                'plugin_id': UCTT_PLUGIN_ID_DUMMY,
                'clients': {
                    'one': {
                        'plugin_id': 'dummy',
                        'arguments': {
                            'outputs': {
                                'dummy' : {
                                    "plugin_id": "text",
                                    "arguments": {
                                        "text": "client dummy output one"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            'workloads' : {
                'workloads': {
                    'one': {
                        'plugin_id': UCTT_PLUGIN_ID_DUMMY,
                    },
                    'two': {
                        'plugin_id': UCTT_PLUGIN_ID_DUMMY,
                        'arguments': {
                            'outputs': {
                                'one' : {
                                    "plugin_id": "text",
                                    "arguments": {
                                        "text": "client two dummy output one"
                                    }
                                }
                            },
                            'clients': {
                                'dummy': {
                                    'plugin_id': UCTT_PLUGIN_ID_DUMMY
                                }
                            }
                        }
                    }
                }
            },
            "dummy": {
                "1": "dummy one"
            }
        })

        return config

    def _dummy_provisioner(self):
        """ Create a config object, and then create a provisioner from it """
        config = self._dummy_config()
        return uctt.new_provisioner_from_config(config)

    def _dummy_workloads(self):
        """ Create a config object, and then get workloads """
        config = self._dummy_config()
        return uctt.new_workloads_from_config(config)

    """ Tests """

    def test_dummy_config_basics(self):
        """ some sanity testing on the shared config object """
        config = self._dummy_config()

        dummy_config = config.load("dummy")
        assert dummy_config.get("1") == "dummy one"

        workload_config = config.load("workloads", validator="jsonschema:dummy.workloads")

    def test_provisioner_sanity(self):
        """ some sanity testing on loading a provisioner """
        provisioner = self._dummy_provisioner()
        assert isinstance(provisioner, DummyProvisionerPlugin)

    def test_provisioner_workflow(self):
        """ test that the provisioner can follow a decent workflow """
        provisioner = self._dummy_provisioner()

        provisioner.prepare()
        provisioner.apply()

        # ...

        provisioner.destroy()

    def test_workloads_sanity(self):
        """ test that we can load the workloads """
        workloads = self._dummy_workloads()

        workload_one = workloads.get_plugin(instance_id="one")
        assert isinstance(workload_one, DummyWorkloadPlugin)

        with self.assertRaises(KeyError):
            workloads["does.not.exist"]

    def test_workloads_outputs(self):
        """ test that the dummy workload got its outputs from configuration """
        workloads = self._dummy_workloads()
        workload_two = workloads.get_plugin(instance_id="two")

        assert workload_two.get_output(instance_id="one").get_output() == "client two dummy output one"

    def test_provisioner_clients(self):
        """ test that the provisioner produces the needed clients """
        provisioner = self._dummy_provisioner()
        provisioner.prepare()

        # two ways to get the same client in this case
        client_one = provisioner.get_client(instance_id="one")
        assert client_one.instance_id == "one"
        client_dummy = provisioner.get_client(plugin_id="dummy")
        assert client_dummy.instance_id == "one"

    def test_clients(self):
        """ test that the provisioner clients behave like clients """
        provisioner = self._dummy_provisioner()
        provisioner.prepare()

        client_one = provisioner.get_client(instance_id="one")

        client_one_output = client_one.get_output(instance_id="dummy")
        assert client_one_output.get_output() == "client dummy output one"
