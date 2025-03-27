from .serializers import CustomTokenObtainPairSerializer, CustomUserResponseSerializer, CustomUserRequestSerializer

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.utils.permissions import UserPermission
from apps.accounts.services.services import UserService, AuthService, GroupService

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        response = Response({
            'refresh': refresh,
            'access': access,
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,
            samesite='None',
            max_age=60 * 5,
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='None',
            max_age=60 * 60 * 24 * 90,
        )

        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'No refresh token provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({
                'access': access_token,
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=60 * 5,
            )
            
            return response
        except TokenError as e:
            raise InvalidToken(str(e))
        
class CustomTokenLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    service = AuthService()

    def post(self, request):
        self.service.logout(request)

        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

class CustomUserView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    service = UserService()
            
    def get(self, request):
        user_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            users = self.service.get_all_users(request)
            serializer = CustomUserResponseSerializer(users, many=True)
            
            return Response({'users': serializer.data}, status=status.HTTP_200_OK)
        
        user = self.service.get_user_by_id(request, user_id)
        serializer = CustomUserResponseSerializer(user)

        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CustomUserRequestSerializer(data=request.data)

        if serializer.is_valid():
            user = self.service.create_user(serializer.validated_data)
            response = CustomUserResponseSerializer(user)

            return Response({'user': response.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = request.query_params.get('id', None)

        if user_id:
            self.service.delete_user(user_id)
            return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

class GroupListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, UserPermission]
    service = GroupService()

    def get(self, request):
        groups = self.service.get_all_groups(request)
        return Response({'groups': groups}, status=status.HTTP_200_OK)