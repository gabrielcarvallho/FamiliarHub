from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenLogoutView, CustomUserView, GroupListView


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', CustomTokenLogoutView.as_view(), name='token_logout'),
    
    path('users/', CustomUserView.as_view(), name='user'),
    path('groups/', GroupListView.as_view(), name='groups'),
]