from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

class CustomAPIException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A server error occurred."
    default_code = "error"

    def __init__(self, detail=None, status_code=None, code=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail

        if status_code is not None:
            self.status_code = status_code

        if code is not None:
            self.code = code
        else:
            self.code = self.default_code

    def __str__(self):
        return self.detail


class LivestockNotFoundException(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Livestock not found."
    default_code = "livestock_not_found"


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to format API exceptions globally.
    """
    # Call REST framework's default exception handler first
    response = drf_exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        return Response(
            {
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.detail,
                    "code": exc.code,
                }
            },
            status=exc.status_code
        )

    if response is None:
        # Handle non-DRF exceptions
        return Response(
            {
                "success": False,
                "error": {
                    "type": "ServerError",
                    "message": "An unexpected error occurred. Please try again later.",
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Customize the response data
    response.data = {
        "success": False,
        "error": {
            "type": exc.__class__.__name__,
            "message": str(exc),
        }
    }

    return response