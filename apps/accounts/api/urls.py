from django.urls import path
from apps.accounts.api.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenLogoutView,
    UserInvitationView,
    UserInvitationAcceptedView,
    CustomUserView,
    GroupListView,
)


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', CustomTokenLogoutView.as_view(), name='token_logout'),
    
    path('users/', CustomUserView.as_view(), name='user'),
    path('groups/', GroupListView.as_view(), name='groups'),

    path('users/invitation/', UserInvitationView.as_view(), name='invitation_user'),
    path('users/invitation/accepted/', UserInvitationAcceptedView.as_view(), name='invitation_accepted')
]