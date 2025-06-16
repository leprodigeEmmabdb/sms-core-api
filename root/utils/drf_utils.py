from drf_standardized_errors.handler import ExceptionHandler
from rest_framework import pagination

from root.utils.erro_logger import handle_exceptions


def default_err_msg(field, **kwargs):
    min_length = kwargs.get('min_length', 5)
    max_length = kwargs.get('max_length', 500)
    return {'blank': f'Champ {field} obligatoire',
            'required': f'Champ {field} obligatoire',
            'min_length': f'Le Champ  {field} doit avoir au moins {min_length} caractères',
            'max_length': f'Le Champ  {field} ne doit pas depasser {max_length} caractères',
            }


def default_field_attr(field, **kwargs):
    min_length = kwargs.get('min_length', 3)
    max_length = kwargs.get('max_length', 500)
    is_password = kwargs.get('is_password', False)
    write_only = kwargs.get('write_only', False)
    read_only = kwargs.get('write_only', False)
    required = kwargs.get('required', False)
    initial = kwargs.get('initial', '')
    help_text = kwargs.get('help_text', '')
    trim_whitespace = kwargs.get('trim_whitespace', True)
    style = kwargs.get('style', None)

    if is_password:
        style = {'input_type': 'password'}

    return {'write_only': write_only, 'required': required,
            'help_text': '', 'style': style,
            'trim_whitespace': trim_whitespace,
            'max_length': max_length, 'min_length': min_length,
            'initial': initial,
            'error_messages': default_err_msg(initial, **kwargs)},


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'count'
    max_page_size = 30


class DFRExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        handle_exceptions()
        return super().convert_known_exceptions(exc)
