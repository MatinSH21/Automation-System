from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from user_management import views as user_views

urlpatterns = [
    path('register/', user_views.EmployeeRegistrationView.as_view(), name='user-register'),
    path('login/', user_views.EmployeeLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
