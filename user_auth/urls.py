from django.urls import path
from .views import SignupView, LoginView, LogoutView, TokenRefreshView, UserDetails

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-details/', UserDetails.as_view(), name='user_details'),

]