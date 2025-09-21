# apps/core/views.py

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.conf import settings

# Do NOT import serializers at the top of the file to prevent circular imports
# from .serializers import UserSerializer, UserLoginSerializer

def welcome(request):
    return HttpResponse("<h1>Welcome to the Kenyan Payroll System Backend!</h1><p>The server is running. Go to the /admin/ for the admin panel or an API endpoint.</p>")

class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Import the serializer here, inside the method
        from .serializers import UserSerializer
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    API endpoint for user login, which returns an authentication token.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Import the serializer here, inside the method
        from .serializers import UserLoginSerializer

        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            role = 'admin' if user.is_superuser else 'employee'
            return Response({'token': token.key, 'role': role}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    API endpoint to retrieve the current authenticated user's profile.
    Requires authentication via token in the Authorization header.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Import the serializer here, inside the method
        from .serializers import UserSerializer
        
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    """
    API endpoint to log out a user by deleting their authentication token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except settings.AUTH_USER_MODEL.auth_token.RelatedObjectDoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_400_BAD_REQUEST)