from django.urls import path
from user_management import views as user_views

urlpatterns = [
    path('register/', user_views.EmployeeRegistrationView.as_view(), name='user-register'),
    path('login/', user_views.EmployeeLoginView.as_view(), name='user-login'),
    path('logout/', user_views.EmployeeLogoutView.as_view(), name='user-logout'),
    path('', user_views.EmployeeListView.as_view(), name='user-listview'),
]
