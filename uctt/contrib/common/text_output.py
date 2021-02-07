from uctt.output import OutputBase
import logging

logger = logging.getLogger('uctt.contrib.common.output.text')


class TextOutputPlugin(OutputBase):
    """ MTT Output plugin a text output type

    this just gets and sets text

    """

    def arguments(self, text):
        """ Assign text """
        self.text = text

    def get_output(self):
        """ retrieve assigned output """
        if hasattr(self, 'text'):
            return self.text

        raise Exception("No text has been assigned to this output object")
