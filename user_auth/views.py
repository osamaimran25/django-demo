from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework import status

from user_auth.models import CustomUser
from .serializers import UserSerializer, UserLoginSerializer


class SignupView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'An error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                user = CustomUser.objects.filter(email=email).first()
                if user is None or not (user.check_password(password)):
                    return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({'message': 'An error occurred: {}'.format(e.detail)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            OutstandingToken.objects.add(token)
            return Response({"message": "Successfully logged out"})
        except:
            return Response({"error": "Invalid token"}, status=400)
        
class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if isinstance(request.user, AnonymousUser):
                raise APIException("User is not authenticated")

            user_email = request.user.email
            return Response({'email': user_email})

        except APIException as e:
            return Response({'error': str(e)}, status=401)