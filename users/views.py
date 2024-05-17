from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User

from .serializers import UserSerializer

# Create your views here.
class RegistrationAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # email verification
        refresh = RefreshToken.for_user(user)
        token = str(refresh)
        
        try:
            htmly = get_template('email_verification.html')
            d = {
                'domain': get_current_site(request).domain,
                'token': token,
                'protocol': 'https' if request.is_secure() else 'http',
                'base_url': settings.BASE_DIR
            }
            subject = 'Activate your user account.'
            from_email = f'Propulse <{settings.EMAIL_HOST_USER}>'
            to_email = user.email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, "text", from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            None

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPI(APIView):
    def post(self, request, token):
        if token:
            try:
                refresh = RefreshToken(token)
                user = User.objects.get(id=refresh.payload['user_id'])
                user.is_active = True
                user.save()
                return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

