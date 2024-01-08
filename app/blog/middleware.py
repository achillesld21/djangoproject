from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        token = request.COOKIES.get('jwt')
        if response.status_code == 401 and token:
            refresh_token = request.session['refresh_token']
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response.set_cookie(key="jwt", value=access_token, httponly=True, max_age=3600)
        return response