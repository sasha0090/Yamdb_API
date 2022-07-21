from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "api"
router = routers.DefaultRouter()

router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    views.ReviewViewSet,
    basename="reviews",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    views.CommentViewSet,
    basename="comments",
)
router.register(r"users", views.UserViewSet, basename="users")
router.register(
    r'titles', views.TitleViewSet, basename='title')
router.register(
    r'categories', views.CategoryViewSet, basename='category')
router.register(
    r'genres', views.GenreViewSet, basename='genre')

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup", views.signup_new_user, name="signup"),
    path("v1/auth/token", views.get_token, name="token"),
]
