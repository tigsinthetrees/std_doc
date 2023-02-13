"""
Unformatted Module docstring
"""

import enum
from locale import str


class TestClass:
    """

    PURPOSE
    -------

    Class docstring

    FUNCTIONS
    ---------

    - test_fn
    - lorem
    - ipsum

    """
    
    def __init__(self, a_parameter):
        self._test_param = a_parameter

    def test_fn(self, parameter1: str, parameter2):
        """

        PURPOSE
        -------

        Function docstring

        PARAMETERS
        ----------

        :param str parameter1: TODO: document description for parameter parameter1
        :param  parameter2: TODO: document description and type for parameter parameter2
        :returns: TODO: Document the return for function test_fn
        :rtype: TODO: Document return type for function test_fn

        EXCEPTIONS
        ----------

        AttributeError

        TEST TABLE
        ----------

        .. list-table::
          :header-rows: 1

          * - Treat
            - Quantity
            - Description
          * - Albatross
            - 2.99
            - On a stick!
          * - Crunchy Frog
            - 1.49
            - If we took the bones out, it wouldn't be crunchy, now, would it?
          * - Gannet Ripple
            - 1.99
            - On a stick!

        """

        pass
        if False:
            raise AttributeError
        return 1

    def undocumented_function(self) -> str:
        pass

    @property
    def read_only(self):
        return self._test_param

    @property
    def read_write(self):
        return self._test_param

    @read_write.setter
    def read_write(self, j):
        self._test_param = j

    def documented_function(self, a, b):
        """

        PURPOSE
        -------

        Shows how a properly documented function would act

        PARAMETERS
        ----------

        :param str a: first parameter
        :param int b: second parameter
        :returns: Simple string
        :rtype: str

        """

        print("I can do as I am told" + a + str(b))
        return "good"


class _LinkType(enum.Enum):

    AUTHOR = "author"
    SOURCE = "source"
    UNDEFINED = "undefined"
    ASSOCIATE = "associate"


print("hello world!")
print("i am another line")
