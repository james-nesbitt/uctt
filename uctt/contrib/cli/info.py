import logging
from typing import Dict, Any

from uctt.cli import CliBase

logger = logging.getLogger('uctt.cli.info')


class InfoCliPlugin(CliBase):
    """ MTT Cli info plugin

    """

    def fire(self, fixtures: Dict[str, Any]):
        """ return a dict of commands """
        self._fixtures = fixtures

        return {
            'info': self.info
        }

    def info(self, raw: bool = True):
        """ return information about the uctt cli setup """
        return self._info_raw()

    def _info_raw(self):
        """ return dummy output """
        info = """---  UCTT CLI INFO --- \n"""

        info += """-> FIXTURES \n"""
        for (fixture_id, fixture) in self._fixtures.items():
            info += "   {} : {} \n".format(fixture_id, fixture)

        return info
