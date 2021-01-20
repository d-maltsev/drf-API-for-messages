from rest_framework.views import exception_handler
from rest_framework.response import Response

import logging

logging.basicConfig(filename='logs.log', format='%(filename)s: %(message)s',
                    level=logging.INFO)


def get_client_ip(request):
    """
    function to retrieve client information (ip address) from request
    """

    x_forwarded_for: str = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip: str = x_forwarded_for.split(',')[0]
    else:
        ip: str = request.META.get('REMOTE_ADDR')
    return ip


def custom_exception_handler(exc, context):
    """
    custom exception handler to logging client information and request url
    if status code is 429 in file logs.log in root
    """

    response: Response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code']: int = response.status_code
        if response.status_code == 429:
            client_ip: str = get_client_ip(context['request'])
            logging.warning(f"client_ip is {client_ip}")
    return response
