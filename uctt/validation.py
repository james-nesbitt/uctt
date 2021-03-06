"""

Common UCTT Validation

Here we keep common validation schemas, to be used with configerus validation
when receiving config or dicts as a definition of architecture such as fixtures.

Validation patters are added via UCTT bootstrapping, which will load the
bootstrapping function in this module.  The bootstrapping function will add
config for validation of core components.

"""

from configerus.contrib.dict import PLUGIN_ID_SOURCE_DICT
from configerus.contrib.jsonschema.validate import PLUGIN_ID_VALIDATE_JSONSCHEMA_SCHEMA_CONFIG_LABEL

from .environment import Environment

from .plugin import UCTT_PLUGIN_CONFIG_KEY_PLUGIN, UCTT_PLUGIN_VALIDATION_JSONSCHEMA
from .fixtures import UCTT_FIXTURES_CONFIG_FIXTURE_KEY, UCTT_FIXTURE_VALIDATION_JSONSCHEMA

UCTT_VALIDATION_CONFIG_SOURCE_INSTANCE_ID = 'uctt_core_validation'


def bootstrap(env: Environment):
    """ Add UTCC core validation definitions to an environment

    What we do here is collect jsonschema for components such as 'fixture' and
    'plugin' and add it to the environment config as a new source.  Then any
    code interacting with the environment can valdiate config.

    Parameters:
    -----------

    env (Environment) : an environment which should have validation config added
        to.

    """

    # Yes this is impossible to read
    #
    # What we have here is a dict of jsonschemas for UCTT components that need
    # validation.  What we are validating is config sourxe for a plugin/fixture
    # which would be passed into the environment handlers which create fixtures
    # from config.
    #
    # There should be one dict key per componment, with the value being a
    # jsonchema dict definition for that component.
    env.config.add_source(PLUGIN_ID_SOURCE_DICT, UCTT_VALIDATION_CONFIG_SOURCE_INSTANCE_ID, priority=30).set_data({
        PLUGIN_ID_VALIDATE_JSONSCHEMA_SCHEMA_CONFIG_LABEL: {
            UCTT_PLUGIN_CONFIG_KEY_PLUGIN: UCTT_PLUGIN_VALIDATION_JSONSCHEMA,
            UCTT_FIXTURES_CONFIG_FIXTURE_KEY: UCTT_FIXTURE_VALIDATION_JSONSCHEMA
        }
    })
