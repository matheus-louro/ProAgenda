from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CadastroView

urlpatterns = [
    path("cadastro/", CadastroView.as_view(), name="cadastro"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="usuarios/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
