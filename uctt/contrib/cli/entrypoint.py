"""

UCTT CLI setuptools entrypoint

Keep the entrypint minimal, and rely on .cli for real work.

"""

import logging


import fire

from uctt import new_config
from uctt.plugin import Type, Factory
from .base import Base

logger = logging.getLogger('uctt.cli.entrypoint')


def main():
    """ Main entrypoint """
    fire.Fire(Base)


if __name__ == '__main__':
    main()
