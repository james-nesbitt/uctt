from uctt.output import OutputBase
import logging

logger = logging.getLogger('uctt.contrib.common.output.text')


class TextOutputPlugin(OutputBase):
    """ MTT Output plugin a text output type

    this just gets and sets text. Nothing fancy.

    """

    def __init__(self, environment, instance_id, data: str = ''):
        """ Run the super constructor but also set class properties

        Parameters:
        -----------

        data (str) : any string data to be stored

        Raises:
        -------

        A configerus.validate.ValidationError is raised if you passed in a
        validator target and validation failed.

        An AssertionError is raised if you didn't pass in a Dict.

        """
        super(OutputBase, self).__init__(environment, instance_id)

        self.set_text(data)

    def set_text(self, data: str):
        self.text = data

    def get_output(self):
        """ retrieve assigned output


        Returns:
        --------

        The string that was assigned using .arguments()

        Raises:
        -------

        AttributeError if you tried to get text before you have assigned it
        using .arguments()

        """
        return self.text
