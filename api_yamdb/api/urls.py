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
router.register("users", views.UserViewSet, basename="users")
router.register("titles", views.TitleViewSet, basename="title")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("genres", views.GenreViewSet, basename="genre")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", views.signup_new_user, name="signup"),
    path("v1/auth/token/", views.get_token, name="token"),
]
