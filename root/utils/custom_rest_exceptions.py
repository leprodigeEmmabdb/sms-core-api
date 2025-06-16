from rest_framework.views import exception_handler

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler

from root.utils.erro_logger import handle_exceptions


def custom_exception_handler(exc, context):
    print('exception here', flush=True)
    handle_exceptions()
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail={'error': exc.message_dict})
        elif hasattr(exc, 'message'):
            exc = DRFValidationError(detail={'error': exc.message})
        elif hasattr(exc, 'messages'):
            exc = DRFValidationError(detail={'error': exc.messages})

    return drf_exception_handler(exc, context)
    # response = exception_handler(exc, context)
    # handle_exceptions()
    # Now add the HTTP status code to the response.
    # if response is not None:
    #    response.data['status_code'] = response.status_code

    # return response
