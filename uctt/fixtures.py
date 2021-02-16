"""

A set of plugin instances kept as a managed set, we call these fixtures

"""
import logging
from typing import Dict, List, Any

from .plugin import Type

logger = logging.getLogger('uctt.fixtures')

UCTT_FIXTURES_CONFIG_FIXTURES_LABEL = 'fixtures'
""" A centralized configerus load labe for multiple provisioners """

class Fixture:
    """ A plugin wrapper struct that keep metadata about the plugin in a set """

    def __init__(self, plugin: object, type: Type,
                 plugin_id: str, instance_id: str, priority: int):
        """

        Parameters:
        -----------

        fixture : the fixture plugin instance

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        """
        self.type = type
        self.plugin_id = plugin_id
        self.instance_id = instance_id
        self.priority = priority
        self.plugin = plugin


class Fixtures:
    """ A set if plugins as a managed set

    A set of plugins that can be added in an arbitrary order but retrieved
    using filters and sorting.

    """

    def __init__(self):
        self.fixtures = []

    def __len__(self) -> int:
        """ Return how many plugin instances we have """
        return self.count()

    def __getitem__(self, instance_id: str) -> object:
        """ Handle subscription request

        For subscriptions assume that an instance_id is being retrieved and that
        a plugin is desired for return.

        Parameters:
        -----------

        instance_id (str) : Instance instance_id to look for

        Returns:

        Plugin object for highest priority plugin with the matching instance_id

        Raises:
        -------

        KeyError if the key cannot be matched,

        """
        return self.get_plugin(instance_id=instance_id)


    def merge_fixtures(self, merge_from: 'Fixtures'):
        """ merge fixture instances from another Fixtures object into this one

        Parameters:
        -----------

        merge_from (Fixtures) : fixture instance source

        """
        self.fixtures += merge_from.fixtures

    def new_fixture(self, plugin: object, type: Type,
                    plugin_id: str, instance_id: str, priority: int):
        """ Add a new fixture by providing the plugin instance and the metadata

        Create a new Fixture from the passed arguments and add it to the Fixtures set

        Parameters:
        -----------

        plugin : the fixture plugin instance

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        """
        fixture = Fixture(
            type=type,
            plugin_id=plugin_id,
            instance_id=instance_id,
            priority=priority,
            plugin=plugin)
        self.fixtures.append(fixture)
        return fixture

    def add_fixture(self, fixture: Fixture):
        """ Add an existing fixture

        Parameters:
        -----------

        fixture (Fixture) : existing fixture to add

        """
        self.fixtures.append(fixture)
        return fixture

    def count(self, type: Type = None, plugin_id: str = '',
              instance_id: str = ''):
        """ retrieve the first matching fixture object based on filters and priority

        Parameters:
        -----------

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        Returns:
        --------

        The fixture plugin object the sorted plugins that match the passed parameters,

        Raises:
        -------

        KeyError if exception_if_missing is True and no matching fixture was found

        """
        return len(self._filter_instances(
            type=type, plugin_id=plugin_id, instance_id=instance_id))

    def get_plugin(self, type: Type = None, plugin_id: str = '',
                    instance_id: str = '', exception_if_missing: bool = True):
        """ retrieve the first matching fixture object based on filters and priority

        Parameters:
        -----------

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        Returns:
        --------

        The highest priority matched Fixture fixture.
        If now fixtures matched, and exception_if_missing is False, then None

        Raises:
        -------

        KeyError if exception_if_missing is True and no matching fixture was found

        """
        instance = self.get_fixture(type=type, plugin_id=plugin_id, instance_id=instance_id, exception_if_missing=exception_if_missing)

        if not instance is None:
            return instance.plugin


    def get_fixture(self, type: Type = None, plugin_id: str = '',
                instance_id: str = '', exception_if_missing: bool = True):
        """ retrieve the first matching fixture object based on filters and priority

        Parameters:
        -----------

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        Returns:
        --------

        The highest priority matched Fixture fixture.
        If now fixtures matched, and exception_if_missing is False, then None

        Raises:
        -------

        KeyError if exception_if_missing is True and no matching fixture was found

        """
        instances = self.get_fixtures(
            type=type,
            plugin_id=plugin_id,
            instance_id=instance_id)

        if len(instances):
            return instances[0]
        if exception_if_missing:
            raise KeyError("Could not find any matching fixture instances.")
        return None

    def get_plugins(self, type: Type = None, plugin_id: str = '',
                     instance_id: str = '') -> List[object]:
        """ retrieve the first matching fixture object based on filters and priority

        Parameters:
        -----------

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        Returns:
        --------

        A List of sorted Fixture fixture objects that match the arguments,
        possibly empty.

        """
        instances = self.get_fixtures(
            type=type,
            plugin_id=plugin_id,
            instance_id=instance_id)
        return [instance.plugin for instance in instances]

    def get_fixtures(self, type: Type = None, plugin_id: str = '',
                      instance_id: str = '') -> List[Fixture]:
        """ Retrieve an ordered filtered list of Fixtures

        Parameters:
        -----------

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        Returns:
        --------

        A sorted List of Fixture structs that matched the arguments,
        possibly empty.

        """
        instances = self._filter_instances(
            type=type, plugin_id=plugin_id, instance_id=instance_id)
        sorted = sort_instance_list(instances)
        return sorted

    def get_filtered(self, type: Type = None,
                     plugin_id: str = '', instance_id: str = '') -> 'Fixtures':
        """ Get a new Fixtures object which is a filtered subset of this one """
        filtered = Fixtures()
        for instance in self._filter_instances(
                type=type, plugin_id=plugin_id, instance_id=instance_id):
            filtered.add_fixture(instance)
        return filtered

    def _filter_instances(self, type: Type = None,
                          plugin_id: str = '', instance_id: str = ''):
        """ Filter the fixture instances down to a List

        Parameters:
        -----------

        Filtering parameters:

        type (.plugin.Type|str) : Type of plugin
        plugin_id (str) : registry plugin_id
        instance_id (str) : plugin instance identifier

        Returns:
        --------

        An unsorted List of Fixture structs that matched the arguments,
        possibly empty.

        Raises:
        -------

        KeyError if exception_if_missing is True and no matching fixture was found

        """
        matched_instances = []
        for plugin_instance in self.fixtures:
            # Could have one-lined this into a lambda but it would be
            # unreadable

            if plugin_id and not plugin_instance.plugin_id == plugin_id:
                continue
            elif instance_id and not plugin_instance.instance_id == instance_id:
                continue
            elif type and not type == plugin_instance.type:
                continue

            matched_instances.append(plugin_instance)

        return matched_instances


def sort_instance_list(list: List[Fixture]):
    """ Order a list of objects with a priority value from highest to lowest """
    return sorted(list, key=lambda i: 1 / i.priority if i.priority else 0)
