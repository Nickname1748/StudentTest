from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django_registration.backends.activation import views as registration_views
from django.views.generic.base import TemplateView

app_name = 'auth_base'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path(
        "activate/complete/",
        TemplateView.as_view(
            template_name = "django_registration/activation_complete.html"
        ),
        name = "activation_complete"
    ),
    path(
        "activate/<str:activation_key>/",
        registration_views.ActivationView.as_view(
            success_url = reverse_lazy('auth_base:activation_complete')
        ),
        name = "activate"
    ),
    path(
        "register/complete/",
        TemplateView.as_view(
            template_name = 'django_registration/registration_complete.html'
        ),
        name="registration_complete"
    ),
    path(
        "register/closed/",
        TemplateView.as_view(
            template_name="django_registration/registration_closed.html"
        ),
        name="registration_disallowed"
    ),
]