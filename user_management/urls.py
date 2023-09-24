from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from user_management import views as user_views

urlpatterns = [
    path('', user_views.EmployeeListAPIView.as_view(), name='user-list'),
    path('me/', user_views.EmployeeAPIView.as_view(), name='user-info'),
    path('<int:pk>/', user_views.ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('register/', user_views.EmployeeRegistrationAPIView.as_view(), name='user-register'),
    path('login/', user_views.EmployeeLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
