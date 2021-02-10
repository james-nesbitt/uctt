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
from configerus.contrib.dict import PLUGIN_ID_SOURCE_DICT
# UCTT components we will need to access the toolbox
import uctt

from uctt.instances import PluginInstances
# We import this so that we don't need to guess on plugin_ids, but not needed
from uctt.contrib.dummy import UCTT_PLUGIN_ID_DUMMY

# imports used only for type testing
from uctt.provisioner import UCTT_PROVISIONER_CONFIG_PROVISIONERS_LABEL, UCTT_PROVISIONER_CONFIG_PROVISIONER_LABEL
from uctt.client import UCTT_CLIENT_CONFIG_CLIENTS_LABEL, UCTT_CLIENT_CONFIG_CLIENT_LABEL
from uctt.workload import UCTT_WORKLOAD_CONFIG_WORKLOADS_LABEL, UCTT_WORKLOAD_CONFIG_WORKLOAD_LABEL

from uctt.contrib.dummy.provisioner import DummyProvisionerPlugin
from uctt.contrib.dummy.client import DummyClientPlugin
from uctt.contrib.dummy.workload import DummyWorkloadPlugin

logger = logging.getLogger("test_dummy")
logger.setLevel(logging.INFO)

""" Contents of test config files used as the source for a config object """

""" TESTS """


class ConfigTemplating(unittest.TestCase):

    def _dummy_config(self):
        """ Create a config object for dummy conventions """

        config = configerus.new_config()
        uctt.bootstrap(config, ['uctt_dummy'])  # not strictly necessary
        return config

    def test_1_construct_dicts(self):
        """ some sanity tests on constructors based on dicts """
        config = self._dummy_config()

        plugin_dict = {
            'plugin_id': UCTT_PLUGIN_ID_DUMMY,
        }

        self.assertIsInstance(
            uctt.new_provisioner_from_dict(
                config=config,
                provisioner_dict=plugin_dict),
            DummyProvisionerPlugin)
        self.assertIsInstance(
            uctt.new_client_from_dict(
                config=config,
                client_dict=plugin_dict),
            DummyClientPlugin)
        self.assertIsInstance(
            uctt.new_workload_from_dict(
                config=config,
                workload_dict=plugin_dict),
            DummyWorkloadPlugin)

        plugins_dict = {
            'one': plugin_dict,
            'two': plugin_dict,
            'three': plugin_dict,
        }

        provisioners = uctt.new_provisioners_from_dict(
            config=config, provisioner_list=plugins_dict)

        self.assertIsInstance(provisioners, PluginInstances)
        self.assertEqual(len(provisioners), 3)

        two = provisioners.get_plugin(instance_id='two')

        self.assertIsInstance(two, DummyProvisionerPlugin)

    def test_3_construct_config(self):
        """ test that we can construct plugins from config """
        config = self._dummy_config()

        plugin_dict = {
            'plugin_id': UCTT_PLUGIN_ID_DUMMY,
        }
        plugins_dict = {
            'one': plugin_dict,
            'two': plugin_dict,
            'three': plugin_dict,
        }

        config.add_source(PLUGIN_ID_SOURCE_DICT, priority=80).set_data({
            UCTT_PROVISIONER_CONFIG_PROVISIONERS_LABEL: plugins_dict,
            UCTT_CLIENT_CONFIG_CLIENTS_LABEL: plugins_dict,
            UCTT_WORKLOAD_CONFIG_WORKLOADS_LABEL: plugins_dict,

            UCTT_PROVISIONER_CONFIG_PROVISIONER_LABEL: plugin_dict,
            UCTT_CLIENT_CONFIG_CLIENT_LABEL: plugin_dict,
            UCTT_WORKLOAD_CONFIG_WORKLOAD_LABEL: plugin_dict
        })

        self.assertIsInstance(
            uctt.new_provisioner_from_config(
                config=config),
            DummyProvisionerPlugin)
        self.assertIsInstance(
            uctt.new_client_from_config(
                config=config),
            DummyClientPlugin)
        self.assertIsInstance(
            uctt.new_workload_from_config(
                config=config),
            DummyWorkloadPlugin)

        provisioners = uctt.new_provisioners_from_config(config=config)

        self.assertIsInstance(provisioners, PluginInstances)
        self.assertEqual(len(provisioners), 3)

        two = provisioners.get_plugin(instance_id='two')

        self.assertIsInstance(two, DummyProvisionerPlugin)
