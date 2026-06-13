from django.urls import path

from .views import RegisterView

# Routes for the companies app (register, login).
urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
]
