import json
from django.utils.deprecation import MiddlewareMixin
from .models import RequestHistory

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            RequestHistory.objects.create(
                user=request.user,
                path=request.path,
                method=request.method,
                status_code=response.status_code,
                response_body=response.content.decode('utf-8') if response.content else ''
            )
        return response