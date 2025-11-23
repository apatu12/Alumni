from urllib.parse import urlencode
from django.utils.deprecation import MiddlewareMixin


class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response


class PreviousURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Simpan HTTP_REFERER (halaman sebelumnya) ke session
        previous = request.META.get('HTTP_REFERER')
        request.session['previous_url'] = previous

        response = self.get_response(request)
        return response
