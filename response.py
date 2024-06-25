import json

from starlette.responses import JSONResponse


class APIResponse:
    """
        A utility class to generate JSON responses for API endpoints.

        This class provides static methods to generate both error and success JSON responses
        with appropriate messages, data, and status codes.
    """

    @staticmethod
    def error_response(err, status_code):
        """
            Creates an error JSON response with a message based on the error type.

            Args:
                err (bytes or str): The error message or bytes object (JSON-encoded).
                status_code (int): The HTTP status code to return.

            Returns:
                JSONResponse: The JSON response containing the error message and status code.
        """
        error = err
        if isinstance(err, bytes):
            error_dict = json.loads(err.decode("utf-8"))
            error = error_dict
        elif isinstance(err, str):
            error = str(err)
        return JSONResponse(content={"message": error, 'data': {}, 'code': status_code}, status_code=status_code)

    @staticmethod
    def success_response(data, msg, status_code):
        """
            Creates a success JSON response with provided data and message.

            Args:
               data (dict): The data to include in the response.
               msg (str): The success message.
               status_code (int): The HTTP status code to return.

            Returns:
               JSONResponse: The JSON response containing the success message, data, and status code.
        """
        return JSONResponse(content={"message": msg, 'data': data, 'code': status_code}, status_code=status_code)

