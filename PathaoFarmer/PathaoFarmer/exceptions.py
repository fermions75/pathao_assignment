from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to format API exceptions globally.
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    # If the exception is already handled by DRF, customize the response
    if response is not None:
        response.data = {
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc),
            }
        }
    else:
        # Handle non-DRF exceptions (e.g., server errors)
        response = Response(
            {
                "success": False,
                "error": {
                    "type": "ServerError",
                    "message": "An unexpected error occurred. Please try again later.",
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
