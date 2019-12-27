"""URLs for login."""
from django.urls import path
from login.views import LoginViewSet
from django.views.generic import TemplateView

urlpatterns = [
    path('home',TemplateView.as_view(template_name='login.html'),name = "home"),
    path('login', LoginViewSet.as_view({'get': 'login'})),
    path('pass-login', LoginViewSet.as_view({'get': 'pass_login'})),
    path('login/get-user', LoginViewSet.as_view({'get': 'get_user'})),
    path('logout', LoginViewSet.as_view({'get': 'logout'}),name = "logout"),
]
