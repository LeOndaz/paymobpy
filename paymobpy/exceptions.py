class PaymobError(Exception):
    """A wrapper around exception for errors from paymob API"""

    def __init__(self, *args, response=None, wrapped_exception=None):
        self.response = response
        self.wrapped_exception = wrapped_exception
        super().__init__(*args)
