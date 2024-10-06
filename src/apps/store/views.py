import logging

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


logger = logging.getLogger('my_middleware_logging')


def index(request: HttpRequest) -> HttpResponse:
    logger.info('Работает index')
    return HttpResponse(content='Hello world!')
