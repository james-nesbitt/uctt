import logging
from typing import Dict

from configerus.contrib.dict import PLUGIN_ID_SOURCE_DICT
from configerus.loaded import LOADED_KEY_ROOT
from uctt.output import OutputBase

logger = logging.getLogger('uctt.contrib.common.output.dict')


class DictOutputPlugin(OutputBase):
    """ MTT Output plugin a Dict output type

    This output plugin leverages configurators features, treating the dict as
    a config source, in order to get validation and navigations.

    """

    def arguments(self, data: Dict, validator: str = ''):
        """ Assign data

        This turns the data into a dict configerus source and adds it to the
        configerus Config object, using a unique load() label.
        The unique label keeps the data separate, but still accessible.

        a configerus LoadedConfig object is kept for the config, which can
        be validated if you passed a validator.

        Parameters:
        -----------

        data (Dict) : any dict data to be stored

        validator (str) : a configerus validator target if you want valdiation
            applied to the data as it is added.

        """
        self.config_instance_id = 'dict-output-{}'.format(self.instance_id)
        self.config.add_source(PLUGIN_ID_SOURCE_DICT, self.config_instance_id).set_data({
            self.config_instance_id: data
        })
        self.loaded_config = self.config.load(
            self.config_instance_id, validator=validator)

    def get_output(self, key: str = LOADED_KEY_ROOT, validator: str = ''):
        """ retrieve an output

        Because we treated that data as a high-priority configerus source with
        a custom label, we can retrieve data from that source easily and also
        leverage other configerus options such as templating and validation

        If you don't pass a key, you will get the entire data value

        Parameters:
        -----------

        key (str) : you can optionally pass a key to retrieve only a part of the
            data structure.  This uses the configerus .get() command which uses
            dot "." notation to descend a tree.

        valdiator (str) : you can tell configerus to apply a validator to the
            return value

        """
        if hasattr(self, 'loaded_config'):
            return self.loaded_config.get(key, validator=validator)

        raise Exception("No data has been assigned to this output object")
