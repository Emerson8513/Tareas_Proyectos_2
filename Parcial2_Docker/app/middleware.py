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
    

    # class RequestLoggingMiddleware(MiddlewareMixin):
    # def process_response(self, request, response):
    #     if request.user.is_authenticated:
    #         # Verificamos si la respuesta es un FileResponse
    #         if isinstance(response, FileResponse):
    #             # Usamos streaming_content para construir el cuerpo de la respuesta
    #             response_body = ''.join(chunk.decode('utf-8') for chunk in response.streaming_content)
    #         else:
    #             # Usamos content para respuestas normales
    #             response_body = response.content.decode('utf-8') if response.content else ''
            
    #         # Guardamos el historial de la solicitud en la base de datos
    #         RequestHistory.objects.create(
    #             user=request.user,
    #             path=request.path,
    #             method=request.method,
    #             status_code=response.status_code,
    #             response_body=response_body
    #         )
    #     return response
