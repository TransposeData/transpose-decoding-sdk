class ContractError(Exception):
    """
    The ContractError exception class is raised for errors that 
    occur during contract execution.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the exception class.

        :param message: The error message.
        """
        
        self.message = message

    
    def __str__(self) -> str:
        """
        Return the string-formated error message.

        :return: The error message.
        """
        
        return 'ContractError ({})'.format(self.message)


class StreamError(Exception):
    """
    The StreamError exception class is raised for errors that 
    occur when during stream execution.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the exception class.

        :param message: The error message.
        """
        
        self.message = message

    
    def __str__(self) -> str:
        """
        Return the string-formated error message.

        :return: The error message.
        """
        
        return 'StreamError ({})'.format(self.message)


class TransposeAPIError(Exception):
    """
    The TransposeAPIError exception class is raised for errors that occur 
    when calling the Transpose API. Each error returned by the API has
    a status code and a message.
    """

    def __init__(self, status_code: int, message: str) -> None:
        """
        Initialize the exception class.

        :param status_code: The status code returned by the API.
        :param message: The error message returned by the API.
        """
        
        self.status_code = status_code
        self.message = message

    
    def __str__(self) -> str:
        """
        Return the string-formated error message.

        :return: The error message.
        """
        
        return 'TransposeAPIError ({}, {})'.format(self.status_code, self.message)