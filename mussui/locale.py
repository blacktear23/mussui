import logging
from django.conf import settings


class DefaultLocalSetterMiddle(object):
    def __init__(self):
        self.default_language = settings.LANGUAGE_CODE
        self.language_cookie = settings.LANGUAGE_COOKIE_NAME

    def process_request(self, request):
        request.need_set_cookie = False
        lang_code = request.COOKIES.get(self.language_cookie, None)
        if lang_code is None:
            request.COOKIES[self.language_cookie] = self.default_language
            request.need_set_cookie = True
        referer = request.META.get('HTTP_REFERER', None)
        if referer is not None and referer.find("speedycloud.cc") >= 0:
            request.COOKIES[self.language_cookie] = 'en'
            request.need_set_cookie = True

    def process_response(self, request, response):
        if getattr(request, 'need_set_cookie', False):
            response.set_cookie(self.language_cookie, request.COOKIES[self.language_cookie])
        return response
