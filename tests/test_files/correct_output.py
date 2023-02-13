"""

PURPOSE
-------

TODO: Document purpose for module test_input.py

CLASSES
-------

.. list-table::
  :header-rows: 1

  * - Class Name
    - Purpose
  * - TestClass
    - Class docstring
  * - _LinkType
    - undocumented

TEMP NOTES
----------

TODO: move these notes into a section with a header
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

    .. list-table::
      :header-rows: 1

      * - Function Name
        - Purpose
      * - test_fn
        - Function docstring
      * - undocumented_function
        - undocumented
      * - documented_function
        - Shows how a properly documented function would act

    """

    def __init__(self, a_parameter):
        """

        PARAMETERS
        ----------

        :param  a_parameter: TODO: document description and type for parameter a_parameter

        """

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
        """

        PURPOSE
        -------

        TODO: Document purpose for function undocumented_function

        """

        pass

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
    """

    PURPOSE
    -------

    TODO: Document purpose for class _LinkType

    PARENT CLASS
    ------------

    enum.Enum

    """

    AUTHOR = "author"
    SOURCE = "source"
    UNDEFINED = "undefined"
    ASSOCIATE = "associate"


print("hello world!")
print("i am another line")
