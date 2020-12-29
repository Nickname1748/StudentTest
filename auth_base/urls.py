from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

app_name = 'auth_base'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout')
]