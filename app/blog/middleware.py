from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        token = request.COOKIES.get('jwt')


        if response.status_code == 401 and token:
            user = self.request.user
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            
            if RefreshToken(refresh_token)['exp'] < timezone.now():
                authentication = JWTAuthentication()

                user, _ = authentication.authenticate(request)
                
                if user:
                    new_access_token = RefreshToken.for_user(user).access_token

                    response.data['access'] = str(new_access_token)
                    print(new_access_token)
                    response.set_cookie('jwt', str(new_access_token), httponly=True)

        return response

    def is_access_token_expired(access_token):
        try:
            refresh_token = RefreshToken(access_token)
            return refresh_token.is_expired
        except Exception:
            return False