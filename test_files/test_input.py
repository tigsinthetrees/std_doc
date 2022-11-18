"""
Module docstring
"""
from locale import str


class TestClass:
    """

    PURPOSE
    --------

    Class docstring

    FUNCTIONS
    ---------

    - test_fn
    - lorem
    - ipsum

    """

    def test_fn(self, parameter1: str, parameter2):
        """
        extra text

        PURPOSE
        --------

        Function docstring

        TEST TABLE
        ---- -----

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


print("hello world!")
print("i am another line")
