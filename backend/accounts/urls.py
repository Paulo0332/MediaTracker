from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name = "accounts/login.html", redirect_authenticated_user = True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
