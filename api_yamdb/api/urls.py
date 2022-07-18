from django.urls import include, path

from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(r"users", views.UserViewSet, basename="users")


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup", views.signup_new_user, name="signup"),
    path("v1/auth/token", views.get_token, name="token"),
]
