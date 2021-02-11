import logging
import os
import importlib.util
import sys

from uctt import new_config
from uctt.plugin import Type, Factory
from uctt.instances import PluginInstances


logger = logging.getLogger('uctt.cli.base')

UCC_CLI_FIXTURE_KEY_CONFIG = 'config'

FILES = {
    'uctt': 'uctt.py',
    'ucttc': 'ucttc.py',
}


class Base:
    """ A Fire compatible base component """

    def __init__(self):

        self._fixtures = {}
        """ CLI Fixtures, plugins instances usable for cli actions """
        self._paths = {}
        """ key value pair of paths to module namespaces where we can look for injection """

        # Look for any paths that we can use to source init code
        self._add_project_root_path()
        # run any init code found in _paths to get ourselves in a state that
        # matches a project
        self._project_init()

        # make sure that we have a sane fixture set
        if not len(self._fixtures):
            logger.warn(
                'UCTT cli was run in a context that provided no fixtures.  This usually means that you are running in a path with no parent ucttc.py file')
            self.fixtures[UCC_CLI_FIXTURE_KEY_CONFIG] = new_config()

        # collect any comands from all discovered cli plugins
        self._collect_commands()

    def _collect_commands(self):
        """ collect commands from all cli plugins

        Get an instance of any registered cli plugin.
        From the plugin, collect the commands and add each command to this
        object directly, so that Fire can see them.

        """

        config = self._fixtures[UCC_CLI_FIXTURE_KEY_CONFIG]
        instances = PluginInstances(config)

        for plugin_id in Factory.registry[Type.CLI.value]:
            logger.info("loading cli plugin: {}".format(plugin_id))
            plugin = instances.add_plugin(
                type=Type.CLI,
                plugin_id=plugin_id,
                instance_id=plugin_id,
                priority=config.default_priority())

            if hasattr(plugin, 'fire'):
                try:
                    commands = plugin.fire(self._fixtures)
                except TypeError as e:
                    raise NotImplementedError(
                        "Plugin {} did not implement the correct fire(fixtures) interface: {}".format(
                            plugin_id, e)) from e

                if not isinstance(commands, dict):
                    raise ValueError(
                        "Plugin returned invalid commands : {}".format(commands))

                ValueError(
                    "Plugin returned invalid commands : {}".format(commands))

                for (command_name, command) in commands.items():
                    logger.debug(
                        "adding cli plugin command: {}->{}".format(plugin_id, command_name))
                    setattr(self, command_name, command)

    def _project_init(self):
        """ initialize the project by looking for path base injections

        fixtures: does any path point to finding fixture declarations

        """
        if len(self._paths):
            for (path_module_name, path) in self._paths.items():
                for (file_module_name, file) in FILES.items():
                    module_name = '{}.{}'.format(
                        path_module_name, path_module_name)
                    module_path = os.path.join(path, file)

                    logger.debug(
                        "Checking for fixtures in: {}".format(module_path))

                    if os.path.isfile(module_path):
                        # the mock-0.3.1 dir contains testcase.py, testutils.py
                        # & mock.py
                        if path not in sys.path:
                            sys.path.append(path)

                        spec = importlib.util.spec_from_file_location(
                            module_name, module_path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        if hasattr(module, 'fixtures'):
                            for (fixture_name,
                                 fixture) in module.fixtures().items():
                                self._fixtures[fixture_name] = fixture

                        else:
                            logger.error('ucttc module has no fixtures')

    def _add_project_root_path(self):
        """ Find a string path to the project root

        Start at the cdw and search upwards until we find a path that contains
        one of the Marker files in FILES

        """

        check_path = os.path.abspath(os.getcwd())
        while check_path:
            if check_path == '/':
                break

            for marker_file in FILES.values():
                marker_path = os.path.join(check_path, marker_file)
                if os.path.isfile(marker_path):
                    self._paths['pwd'] = check_path
                    return

    # def dummy(self):
    #     """ Dummy command """
    #     print("You dummy")


""" Try to discover fixtures """
