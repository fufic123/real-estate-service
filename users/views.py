from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from .models import User

from .serializers import UserSerializer



# Create your views here.
class RegistrationAPI(APIView):
    def post(self, request):
        required_fields = ['name', 'surname', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            error_msg = f"{', '.join(missing_fields)} {'was' if len(missing_fields) == 1 else 'were'} not provided"
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if 'email' in e.message_dict:
                return Response({"error": "User with this email already exist."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        
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

        return Response({"message": "Activation letter sent to your email."}, status=status.HTTP_200_OK)



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


class SocialSettingsAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        user = request.user
        
        website = request.query_params.get("website")
        instagram = request.query_params.get("instagram")
        facebook = request.query_params.get("facebook")
        
        try:
            if website is not None:
                user.website = website
            if instagram is not None:
                user.instagram = instagram
            if facebook is not None:
                user.facebook = facebook
            user.full_clean()
            user.save()
        except ValidationError as e:
            errors = e.message_dict
            for field, messages in errors.items():
                for message in messages:
                    if message.startswith('Ensure this value has at most'):
                        return Response({"error": f"{field} URL is too long"}, status=status.HTTP_400_BAD_REQUEST)
                    elif message == 'Enter a valid URL.':
                        return Response({"error": f"{field} URL is not valid"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "User social links updated successfully."}, status=status.HTTP_200_OK)


class GetUserAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)