import logging
import time, json
import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from django.http import HttpResponseForbidden, HttpResponseNotAllowed

logger = logging.getLogger(__name__)

regex = re.compile('^HTTP_')
regex_http_ = re.compile(r'^HTTP_.+$')
regex_content_type = re.compile(r'^CONTENT_TYPE$')
regex_content_length = re.compile(r'^CONTENT_LENGTH$')


class APILoggerMiddleWare(MiddlewareMixin):
    LOG = '%(PATH_INFO)s (%(REQUEST_METHOD)s, time: %(time)s, user id: %(user_id)s, db queries: %(db_queries)s): %(body)s'
    LOGGER_NAME = getattr(settings, 'API_LOGGER_NAME', 'citrus_logger')
    context = None

    def is_api_request(self, request):
        """
        checks if request is an api request
        """
        return request.META['PATH_INFO'].startswith('/garden/')

    def get_user_id(self, request):
        """
        get user:
        + from request
        + or using token from request header
        """
        user = getattr(request, 'user', None)
        if user and user.is_authenticated():
            return user.id
        # try:
        #     key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        #     token = Token.objects.get(key=key)
        # except:
        #     return '-'
        # else:
        #     return token.user.id

    def process_request(self, request):
        context = request.META.copy()
        context.update({
            'user_id': '-',
            'time': 'unknown',
            'body': '',
            'db_queries': '-'
        })

        if self.is_api_request(request):
            if request.method == 'GET':
                context.update({'body': 'DATA: ' + str(request.GET.dict())})
            elif request.method in ('POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'):
                if request.method == 'POST':
                    body = str(request.POST.dict())
                else:
                    # if request is PUT or PATCH we don't have data parsed in
                    # PUT or PATCH so we need to save body of request
                    body = getattr(request, 'body', '')
                context.update({'body': 'DATA: ' + body})

            request.api_start_time = time.time()
            request.api_logger_context = context

    def process_response(self, request, response):
        context = getattr(request, 'api_logger_context', {})
        if self.is_api_request(request) and context:
            if getattr(request, 'api_start_time', None):
                t = time.time() - request.api_start_time
                context.update({'time': t})
            self._update_context(request, response)

            self._log(context)
        request.api_start_time = None
        return response

    def _update_context(self, request, response):
        context = getattr(request, 'api_logger_context', {})
        context.update({
            'user_id': self.get_user_id(request),
            'db_queries': len(connection.queries)
        })
        request.api_logger_context = context

    def _get_logger(self):
        return logging.getLogger(self.LOGGER_NAME)

    def _log(self, context):
        logger = self._get_logger()
        logger.info(self.LOG % context)


class RequestParamsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # assign citrus_content property to the request
        # to hold the request params
        request.params = None
        print('')
        if request.method == 'GET':
            request.params = request.GET.dict()
            #print('PARAMS GET', request.params)

        elif request.method == 'POST':
            request.params = request.POST.dict()
            #print('PARAMS POST', request.params)

        if not request.params and request.body:
            try:
                request.params = json.loads(str(request.body.decode("utf-8")))
                #print('PARAMS BODY', request.params)

            except Exception as err:
                request.params = None

        # set the PSEUDO if the request is of type psuedo.

        # is_pseudo = request.META.get('HTTP_PSUEDO', False)
        # if is_pseudo:
        if any(key in request.META for key in ['HTTP_PSUEDO', 'HTTP_PSEUDO']):
            request.pseudo = True
        else:
            request.pseudo = False
        #print(' => REQUESTED PARAMS ', request.params)
        return None