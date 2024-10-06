import logging
import time

logger = logging.getLogger('my_middleware_logging')


class LoggingMiddleware:
    """Посредник"""
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        logger.debug('Обработка поступившего запроса в LoggingMiddleware')
        time_start = time.time()

        response = self._get_response(request)

        logger.debug('Обработка ответа в LoggingMiddleware')
        time_finish = time.time()
        logger.debug(f'Время, затраченное на выполнение запроса: {time_finish - time_start}')

        return response
