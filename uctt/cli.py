"""

CLI Plugins base

@see ./cli for the cli implementation

"""
import logging

import uctt
from uctt.plugin import UCTTPlugin, Type

logger = logging.getLogger('uctt.cli')

UCTT_PLUGIN_TYPE_CLI = Type.CLI
""" Fast access to the output plugin type """


class CliBase(UCTTPlugin):
    """ Base class for cli plugins """
    pass

    def exec(self):
        """ this plugin can execute """
        raise NotImplemented("this functionality has not yet been written.")
