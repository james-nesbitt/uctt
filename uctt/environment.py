"""

An environment is meant to represent a testable cluster as a testing harness

In UCTT an environment is a single configerus Config object and a set of
UCTT plugins in a manageable set.

UCTT uses the Fixtures object to manage a set of plugins, which allows us to
mix a bunch of plugin objects of different types together and manage them.

"""
import logging
import random
import string
from typing import List, Dict, Any

from configerus.config import Config
from configerus.loaded import Loaded, LOADED_KEY_ROOT
from configerus.validator import ValidationError

from .plugin import (
    Factory,
    Type,
    UCTTPlugin,
    UCTT_PLUGIN_CONFIG_KEY_TYPE,
    UCTT_PLUGIN_CONFIG_KEY_PLUGINID,
    UCTT_PLUGIN_CONFIG_KEY_INSTANCEID,
    UCTT_PLUGIN_CONFIG_KEY_ARGUMENTS,
    UCTT_PLUGIN_CONFIG_KEY_PRIORITY,
    UCTT_PLUGIN_CONFIG_KEY_CONFIG,
    UCTT_PLUGIN_CONFIG_KEY_VALIDATORS)
from .fixtures import (
    Fixtures,
    Fixture,
    UCTT_FIXTURES_CONFIG_FIXTURE_KEY,
    UCTT_FIXTURES_CONFIG_FIXTURES_LABEL)


import logging

logger = logging.getLogger('uctt.environment')

DEFAULT_PLUGIN_PRIORITY = 70
""" Default plugin priority when turned into a fixture """

FIXTURE_VALIDATION_TARGET_FORMAT_STRING = 'jsonschema:{key}'


class Environment:
    """ A testing environment, usually composed of a config and plugins """

    def __init__(self, config: Config):
        """

        Parameters:
        -----------

        config (configerus.Config) : A single config object which will be used
            to define the environment.

        """

        self.config = config
        """ Config object that defines the environment """
        self.fixtures = Fixtures()
        """ fixtures/plugins that can interact with the environment """
        self.default_plugin_priority = DEFAULT_PLUGIN_PRIORITY

    def plugin_priority(self, delta: int = 0):
        """ Return a default pluging priority with a delta """
        return DEFAULT_PLUGIN_PRIORITY + delta

    """

    Generic Plugin construction

    """

    def add_fixtures_from_typeconfig(
            self, label: str, base: Any = LOADED_KEY_ROOT, validator: str = '') -> Fixtures:
        """ Create multiple different fixtures from a structured config source

        This approach to creating fixtures keeps a tree:

        {type}:
            {instance_id}:
                ... {instance config} ...

        Parameters:
        -----------

        config (Config) : Used to load and get the plugin configuration

        label (str) : config label to load to pull plugin configuration. That
            label is loaded and config is pulled to produce a list of plugins

        base (str|List) : config key to get a Dict of plugins configurations.  This
            should point to a dict of plugin configurations.
            A list of strings is valid as configerus.loaded.get() can take that as
            an argument.
            We call this base instead of key as we will be searching for sub-paths
            to pull individual elements

        validator (str) : optionally use a configerus validator on the instance
            config/dict before a plugin is created.

        arguments (Dict[str, Any]) : A Dict of named arguments to pass to the
            plugin constructor.  Constructors should be able to work without
            requiring the arguments, but these tend to be pivotal for them.

        Returns:
        --------

        Fixtures of your type

        Raises:
        -------

        If you ask for a plugin which has not been registered, then you're going to
        get a NotImplementedError exception.
        To make sure that your desired plugin is registered, make sure to import
        the module that contains the factory method with a decorator.

        """
        fixtures = Fixtures()
        """ plugin set which will be used to create new plugins """

        try:
            plugin_config = self.config.load(label)
            plugin_type_list = plugin_config.get(
                base, exception_if_missing=True)
        except KeyError as e:
            if exception_if_missing:
                return KeyError(
                    'Could not load any config for plugin generation')
                # there is not config so we can ignore this
            else:
                return fixtures

        # Upper/Outer layer defines plugin type
        for type, plugin_list in plugin_type_list.items():
            # Lower/Inner layer is a list of plugins to create of that type
            for instance_id in plugin_list.keys():
                # This fixture gets effectively added to 2 different Fixtures object.
                # 1. we manually add it to our Fixtures object for this function call
                # 2. the add_fixture_from_config() adds it to the fixture for this
                #    environment object.
                fixture = self.add_fixture_from_config(
                    label=label,
                    base=[base, instance_id],
                    type=type,
                    instance_id=instance_id,
                    validator=validator)
                fixtures.add_fixture(fixture)

        return fixtures

    def add_fixtures_from_config(self, label: str = UCTT_FIXTURES_CONFIG_FIXTURES_LABEL, base: Any = LOADED_KEY_ROOT, type: Type = None, validator: str = '',
                                 exception_if_missing: bool = False, arguments: Dict[str, Any] = {}) -> Fixtures:
        """ Create plugins from some config

        This method will interpret some config values as being usable to build a Dict
        of plugins from.

        Parameters:
        -----------

        config (Config) : Used to load and get the plugin configuration

        label (str) : config label to load to pull plugin configuration. That
            label is loaded and config is pulled to produce a list of plugins

        base (str|List) : config key to get a Dict of plugins configurations.  This
            should point to a dict of plugin configurations.
            A list of strings is valid as configerus.loaded.get() can take that as
            an argument.
            We call this base instead of key as we will be searching for sub-paths
            to pull individual elements

        type (.plugin.Type) : plugin type to create, pulled from the config/dict if
            omitted.  If Type is provided by neither argument nor source then
            you're gonna have a bad time.

        validator (str) : optionally use a configerus validator on the instance
            config/dict before a plugin is created.

        arguments (Dict[str, Any]) : A Dict of named arguments to pass to the
            plugin constructor.  Constructors should be able to work without
            requiring the arguments, but these tend to be pivotal for them.

        Returns:
        --------

        Fixtures of your type

        Raises:
        -------

        If you ask for a plugin which has not been registered, then you're going to
        get a NotImplementedError exception.
        To make sure that your desired plugin is registered, make sure to import
        the module that contains the factory method with a decorator.

        """
        fixtures = Fixtures()
        """ plugin set which will be used to create new plugins """

        try:
            plugin_config = self.config.load(label)
            plugin_list = plugin_config.get(base, exception_if_missing=True)
        except KeyError as e:
            if exception_if_missing:
                raise KeyError(
                    'Could not load any config for plugin generation') from e
                # there is not config so we can ignore this
            else:
                return fixtures

        for instance_id in plugin_list.keys():
            # This fixture gets effectively added to 2 different Fixtures object.
            # 1. we manually add it to our Fixtures object for this function call
            # 2. the add_fixture_from_config() adds it to the fixture for this
            #    environment object.
            fixture = self.add_fixture_from_config(
                label=label,
                base=[base, instance_id],
                type=type,
                instance_id=instance_id,
                validator=validator,
                arguments=arguments)
            fixtures.add_fixture(fixture)

        return fixtures

    def add_fixtures_from_dict(self, plugin_list: Dict[str, Dict[str, Any]], type: Type = None,
                               validator: str = '', arguments: Dict[str, Any] = {}) -> Fixtures:
        """ Create a set of plugins from Dict information

        The passed dict should be a key=>details map of plugins, which will be turned
        into a Fixtures map of plugins that can be used to interact with the
        objects.

        Parameters:
        -----------

        config (Config) : configerus.Config object passed to each generated plugins.

        type (.plugin.Type) : plugin type to create, pulled from the config/dict if
            omitted

        provisioner_list (Dict[str, Dict]) : map of key=> config dicts, where each dict
            contains all of the information that is needed to build the plugin.

            for details, @see add_fixture_from_dict

        validator (str) : optionally use a configerus validator on the instance
            config/dict before a plugin is created.

        arguments (Dict[str, Any]) : A Dict of named arguments to pass to the
            plugin constructor.  Constructors should be able to work without
            requiring the arguments, but these tend to be pivotal for them.

        Returns:
        --------

        A Fixtures object with the plugin objects created

        """
        fixtures = Fixtures()

        if not isinstance(plugin_list, dict):
            raise ValueError(
                'Did not receive a good dict of config to make plugins from: %s',
                plugin_list)

        for instance_id, plugin_dict in plugin_list.items():
            # This fixture gets effectively added to 2 different Fixtures object.
            # 1. we manually add it to our Fixtures object for this function call
            # 2. the add_fixture_from_config() adds it to the fixture for this
            #    environment object.
            fixture = self.add_fixture_from_dict(
                plugin_dict=plugin_dict,
                type=type,
                instance_id=instance_id,
                validator=validator,
                arguments=arguments)
            fixtures.add_fixture(fixture)

        return fixtures

    def add_fixture_from_config(self, label: str, base: Any = LOADED_KEY_ROOT, type: Type = None,
                                instance_id: str = '', priority: int = -1, validator: str = '', arguments: Dict[str, Any] = {}) -> Fixture:
        """ Create a plugin from some config

        This method will interpret some config values as being usable to build plugin

        @see add_fixture_from_loadedconfig

        @note we could validate here instead of passing on the validator, but we
            pass it on to keep parity across a number of cases, and to keep as
            much complex logic in one place.

        Parameters:
        -----------

        config (Config) : Used to load and get the plugin configuration

        type (.plugin.Type) : plugin type to create, pulled from the config/dict if
            omitted. An exception will be thrown if Type is found from neither
            this argument nor the passed config.

        label (str) : config label to load to pull plugin configuration. That
            label is loaded and config is pulled to produce a list of plugins.

        base (str|List) : config key used as a .get() base for all gets.  With this
            you can instruct to pull config from a section of loaded config.
            A list of strings is valid because configerus.loaded.get() can take that
            as an argument. We will be using the list syntax anyway.
            We call this base instead of key as we will be searching for sub-paths
            to pull individual elements.

        instance_id (str) : optionally pass an instance_id for the item.

        validator (str) : optionally use a configerus validator on the entire .get()
            for the instance config.

        Returns:
        --------

        A Fixture object with the new plugin added

        The Fixtures has already been added to the environment, but is returned
        so that the consumer can act on it separately without haveing to
        search for it.

        Raises:
        -------

        If you ask for a plugin which has not been registered, then you're going
        to get a NotImplementedError exception. To make sure that your desired
        plugin is registered, make sure to import the module that contains the
        factory method with a decorator.

        A ValueError is thrown if the plugin cannot be created due to missing
        plugin configuration/argument values.  This means that we could not
        determine how to create the plugin.

        A configerus.validate.ValidationError will be raised if a validation
        target was passed and validation failed.

        """
        try:
            plugin_loaded = self.config.load(label)
        except KeyError as e:
            raise KeyError("Could not load plugin config source.") from e
        """ loaded configuration for the plugin """

        return self.add_fixture_from_loadedconfig(loaded=plugin_loaded, base=base, type=type,
                                                  instance_id=instance_id, priority=priority, validator=validator, arguments=arguments)

    def add_fixture_from_dict(self, plugin_dict: Dict[str, Any], type: Type = None,
                              instance_id: str = '', validator: str = '', arguments: Dict[str, Any] = {}) -> Fixture:
        """ Create a single plugin from a Dict of information for it

        Create a new plugin from a map/dict of settings for the needed parameters.

        @see add_fixture_from_loadedconfig

        Parameters:
        -----------

        config (Config) : configerus.Config object passed to each generated plugins.

        type (.plugin.Type) : plugin type to create, pulled from the config/dict if
            omitted

        client_dict (Dict[str,Any]) : Dict from which all needed information will
            be pulled.  Optionally additional config sources can be included as well
            as arguments which could be passed to the plugin.

            @see add_fixture_from_dict for more details.

        instance_id (str) : optionally pass an instance_id for the item.

        validator (str) : optionally use a configerus validator on the entire .get()
            for the instance config.

        Return:
        -------

        A Fixture object with the new plugin added

        The Fixtures has already been added to the environment, but is returned
        so that the consumer can act on it separately without haveing to
        search for it.

        """
        # Create a mock configerus.loaded.Loaded object, not attached to anything
        # and use it for config retrieval.  This gives us formatting, validation
        # etc.
        mock_config_loaded = Loaded(
            data=plugin_dict,
            parent=self.config,
            instance_id='mock-plugin-construct')
        """ Mock configerus loaded object for config retrieval """
        base = LOADED_KEY_ROOT
        """ to keep this function similar to add_fixture_from_config we use an empty .get() base """

        return self.add_fixture_from_loadedconfig(
            loaded=mock_config_loaded, base=base, type=type, instance_id=instance_id, validator=validator, arguments=arguments)

    def add_fixture_from_loadedconfig(self, loaded: Loaded, base: Any = LOADED_KEY_ROOT, type: Type = None,
                                      instance_id: str = '', priority: int = -1, validator: str = '', arguments: Dict[str, Any] = {}) -> Fixture:
        """ Create a plugin from loaded config

        This method will interpret some config values as being usable to build plugin.
        This function starts with a loaded config object because we can leverage
        that from more starting points.

        Using a configerus config object allows us to leverage advanced configerus
        features such as tree searching, formatting and validation.

        What is looked for:

        1. valdiators if we need to validate the entire label/key before using it
        2. type if we did not receive a type
        3. plugin_id : which will tell us what plugin to load
        4. optional instance_id if none was passed
        5. config if you want config added - ONLY if fixtures is None
           (plugins in Fixtures cannot override config objects)
        6. arguments that will be executed on an argument() method if the
            plugin has it.

        Parameters:
        -----------

        config (Config) : Used to load and get the plugin configuration

        type (.plugin.Type) : plugin type to create, pulled from the config/dict if
            omitted. An exception will be thrown if Type is found from neither
            this argument nor the passed config.

        label (str) : config label to load to pull plugin configuration. That
            label is loaded and config is pulled to produce a list of plugins.

        base (str|List) : config key used as a .get() base for all gets.  With this
            you can instruct to pull config from a section of loaded config.
            A list of strings is valid because configerus.loaded.get() can take that
            as an argument. We will be using the list syntax anyway.
            We call this base instead of key as we will be searching for sub-paths
            to pull individual elements.

        instance_id (str) : optionally pass an instance_id for the item.

        validator (str) : optionally use a configerus validator on the entire .get()
            for the instance config.

        Returns:
        --------

        A Fixture object with the new plugin added

        The Fixtures has already been added to the environment, but is returned
        so that the consumer can act on it separately without haveing to
        search for it.

        Raises:
        -------

        If you ask for a plugin which has not been registered, then you're going
        to get a NotImplementedError exception. To make sure that your desired
        plugin is registered, make sure to import the module that contains the
        factory method with a decorator.

        A ValueError is thrown if the plugin cannot be created due to missing
        plugin configuration/argument values.  This means that we could not
        determine how to create the plugin.

        A configerus.validate.ValidationError will be raised if a validation
        target was passed and validation failed.

        """
        logger.debug(
            'Construct config plugin [{}][{}]'.format(
                type, instance_id))

        # it might be expensive to retrieve all this but we do it to catch early
        # faults in config.
        plugin_base = loaded.get(base)
        if plugin_base is None:
            raise ValueError(
                "Cannot build plugin as provided config was empty.")

        validators = [
            FIXTURE_VALIDATION_TARGET_FORMAT_STRING.format(
                key=UCTT_FIXTURES_CONFIG_FIXTURE_KEY)]
        config_validators = loaded.get(
            [base, UCTT_PLUGIN_CONFIG_KEY_VALIDATORS])
        if config_validators:
            validators = config_validators
        if validator:
            validators.append(validator)
        if len(validators):
            # Run configerus validation on the config base once per validator
            try:
                for validator in validators:
                    loaded.validate(plugin_base, validate_target=validator)
            except ValidationError as e:
                raise e

        if type is None:
            type = loaded.get([base, UCTT_PLUGIN_CONFIG_KEY_TYPE])
        if isinstance(type, str):
            # If a string type was passed in, ask the Type enum to convert it
            type = Type.from_string(type)
        if not type:
            raise ValueError(
                "Could not find a plugin type when trying to create a plugin : {}".format(loaded.get(base)))

        plugin_id = loaded.get([base, UCTT_PLUGIN_CONFIG_KEY_PLUGINID])
        if not plugin_id:
            raise ValueError(
                "Could not find a plugin_id when trying to create a '{}' plugin from config: {}".format(type, loaded.get(base)))

        # if no instance_id was passed, try to load one or just make one up
        if not instance_id:
            instance_id = loaded.get(
                [base, UCTT_PLUGIN_CONFIG_KEY_INSTANCEID])
            if not instance_id:
                instance_id = '{}-{}-{}'.format(type.value, plugin_id, ''.join(
                    random.choice(string.ascii_lowercase) for i in range(10)))

        if priority < 0:
            priority = loaded.get([base, UCTT_PLUGIN_CONFIG_KEY_PRIORITY])
        if not priority:
            priority = self.plugin_priority()
            """ instance priority - this is actually a stupid way to get it """

        # If arguments were given then pass them on
        config_arguments = loaded.get([base, UCTT_PLUGIN_CONFIG_KEY_ARGUMENTS])
        if config_arguments is not None:
            arguments = arguments.copy()
            arguments.update(config_arguments)

        # Use the factory to make the .fixtures.Fixture
        fixture = self.add_fixture(
            type=type,
            plugin_id=plugin_id,
            instance_id=instance_id,
            priority=priority,
            arguments=arguments)
        plugin = fixture.plugin

        return fixture

    def add_fixture(self, type: Type, plugin_id: str,
                    instance_id: str, priority: int, arguments: Dict[str, Any] = {}) -> Fixture:
        """ Create a new plugin from parameters

        Parameters:
        -----------

        config (Config) : configerus.Config object passed to each generated plugins.

        type (.plugin.Type) : plugin type to create.

        plugin_id (str) : UCTT plugin id for the plugin type, to tell us what plugin
            factory to load.

            @see .plugin.Factory for more details on how plugins are loaded.

        instance_id (str) : string instance id that will be passed to the new plugin
            object.

        priority (int) : Integer priority 1-100 for comparative prioritization
            between other plugins.

        arguments (Dict[str, Any]) : Arguments which should be passed to the
            plugin constructor after environment and instance_id

        Return:
        -------

        A Fixture object with the new plugin added

        The Fixtures has already been added to the environment, but is returned
        so that the consumer can act on it separately without haveing to
        search for it.

        Raises:
        -------

        NotImplementedError if you asked for an unregistered plugin_id/type

        """
        fac = Factory(type, plugin_id)
        plugin = fac.create(self, instance_id, **arguments)
        fixture = self.fixtures.new_fixture(
            plugin=plugin,
            type=type,
            plugin_id=plugin_id,
            instance_id=instance_id,
            priority=priority)
        return fixture
